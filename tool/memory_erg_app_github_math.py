import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass, asdict, fields

JST = timezone(timedelta(hours=9))

# =========================
# Output language policy
# =========================

SYSTEM_PROMPT_JA = (
    "あなたは日本語で回答する構造分析アシスタントである。"
    "出力は必ず日本語にする。中国語では回答しない。"
    "固有名詞・技術語以外で中国語表現を使わない。"
    "回答は簡潔に、構造・定義・手順を優先する。"
)

LANGUAGE_CONSTRAINT_JA = "必ず日本語で回答する。中国語で出力してはいけない。"

# =========================
# Node / Edge
# =========================

@dataclass
class Node:
    id: str
    timestamp: str
    project: str
    layer: str
    structure: str
    text: str
    op: str
    features: list
    sigma: list
    structure_features: list
    domain_candidates: list
    recency: int = 3
    branch_degree: int = 0
    locked: bool = False
    source: str = ""

@dataclass
class Edge:
    source: str
    target: str
    type: str

# =========================
# 設定
# =========================

# VSCode/PowerShell のカレントディレクトリに依存しないよう、
# この .py ファイルの隣に memory_store を作る。
BASE_DIR = Path(__file__).resolve().parent
STORE = BASE_DIR / "memory_store"
NODES = STORE / "nodes.jsonl"
EDGES = STORE / "edges.jsonl"

STORE.mkdir(exist_ok=True)

# nodes.jsonl / edges.jsonl を .py と同じ階層に置いていた場合は自動移行。
for name in ["nodes.jsonl", "edges.jsonl"]:
    src = BASE_DIR / name
    dst = STORE / name
    if src.exists() and not dst.exists():
        dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

# =========================
# rules: project / layer / operation / structure / math router
# =========================

PROJECT_RULES = {
    # GIF/DIFはERGに吸収させず、独立探索できるようにする。
    "DIF": ["DIF", "差分構造", "差分", "空スロット", "スロット", "4原理", "四原理", "複数出力"],
    "GIF": ["GIF", "生成", "生成構造", "構造生成", "変換", "操作列生成"],
    "ERG": [
        "ERG", "EGR", "HVM", "メモリ", "memory", "履歴VM",
        "operation", "trace", "自己参照", "layer", "層分離",
    ],
    "CPR": ["CPR", "資源", "トークン", "ログ", "bitmap", "ビットマップ", "trial", "グリッド", "再生", "密度"],
    "math": [
        "数学", "証明", "線形", "定理", "DAG", "固有", "行列", "集合", "群", "圏", "位相",
        "オートマトン", "力学系", "層", "束", "符号", "最適輸送", "書換え", "不動点",
    ],
    "daily": ["京都", "連絡", "DM", "相手", "会話", "返信", "GW"],
    "coding": ["Python", "コード", "app.py", ".py", "VSCode", "PowerShell", "Ollama", "LLM", "ローカルLLM", ".bat", "bat"],
}

KEYWORDS = sorted({
    "ERG", "EGR", "HVM", "GIF", "DIF", "CPR",
    "メモリ", "memory", "履歴VM", "operation_trace", "operation", "trace",
    "ログ", "京都", "連絡", "DM",
    "Python", "コード", "VSCode", "PowerShell", "Ollama", "LLM", "ローカルLLM",
    "数学", "証明", "線形", "DAG", "群", "圏", "位相", "層", "束", "符号", "最適輸送",
    "状態", "意味", "差分", "比較", "パケット", "packet",
    "ビットマップ", "bitmap", "グリッド", "トークン", "再生", "密度",
    "自己参照", "メタ", "meta", "layer", "層分離", "object", "tool",
    "空スロット", "スロット", "複数出力", "対称", "不変", "閉包", "合成", "写像",
    "局所", "大域", "遷移", "反復", "格子", "近傍", "制約", "矛盾", "QR", "書換え", "再帰", "不動点",
}, key=len, reverse=True)

META_WORDS = [
    "ERGでERG", "自己参照", "自己記述", "メタ", "meta", "メタレベル",
    "対象レベル", "層", "layer", "層分離", "ループ", "混線", "再帰",
]

TOOL_WORDS = [
    "Python", "コード", "app.py", ".py", "VSCode", "PowerShell", "Ollama", "LLM", "ローカルLLM",
    ".bat", "bat", "起動", "ターミナル", "実装", "修正", "戻して", "追加", "生成",
    "packet", "パケット", "ask", "query", "rebuild", "status", "launcher", "ランチャー",
]

STRUCTURE_RULES = {
    "slot_generator": ["空スロット", "スロット", "穴埋め", "入力を入れる", "複数出力", "4原理", "四原理"],
    "symmetry_action": ["対称", "入れ替え", "置換", "不変", "同型", "群作用"],
    "graph_relation": ["ノード", "辺", "参照", "分岐", "DAG", "グラフ", "ネットワーク", "隣接", "edge", "node"],
    "algebraic_operation": ["操作", "閉包", "合成", "単位元", "逆", "群", "モノイド", "半群", "代数"],
    "category_diagram": ["対象", "射", "写像", "可換", "図式", "圏", "関手", "自然変換"],
    "local_global": ["局所", "大域", "貼り合わせ", "破綻", "穴", "被覆", "層", "コホモロジー"],
    "state_transition": ["状態", "遷移", "反復", "収束", "周期", "力学", "マルコフ", "オートマトン"],
    "cellular_lattice": ["格子", "セル", "近傍", "CA", "セルオートマトン", "パーコレーション", "グリッド"],
    "order_lattice": ["順序", "包含", "上位", "下位", "束", "半順序", "精緻化"],
    "logic_constraint": ["制約", "一貫性", "矛盾", "充足", "SAT", "論理", "モデル"],
    "coding_information": ["符号", "情報", "QR", "冗長", "誤り訂正", "頑丈", "欠損耐性"],
    "optimization_flow": ["コスト", "流れ", "最適輸送", "最適化", "フロー", "歪み"],
    "rewriting_language": ["書換え", "書き換え", "生成規則", "形式言語", "文法", "操作列"],
    "recursion_fixedpoint": ["自己参照", "再帰", "不動点", "固定点", "ループ"],
}

DOMAIN_BY_STRUCTURE = {
    "slot_generator": ["rewriting_systems", "universal_algebra", "operad", "group_action"],
    "symmetry_action": ["group_action", "invariant_theory", "combinatorics"],
    "graph_relation": ["graph_theory", "DAG", "network_analysis"],
    "algebraic_operation": ["universal_algebra", "semigroup_monoid_group", "abstract_algebra"],
    "category_diagram": ["category_theory", "diagram_chasing"],
    "local_global": ["topology", "sheaf_theory", "cohomology_style"],
    "state_transition": ["dynamical_systems", "automata_theory", "markov_process"],
    "cellular_lattice": ["cellular_automata", "percolation_theory", "stochastic_process"],
    "order_lattice": ["order_theory", "lattice_theory"],
    "logic_constraint": ["logic", "model_theory", "SAT_CSP"],
    "coding_information": ["coding_theory", "information_theory"],
    "optimization_flow": ["optimal_transport", "network_flow", "optimization"],
    "rewriting_language": ["rewriting_systems", "formal_language", "computation_theory"],
    "recursion_fixedpoint": ["fixed_point_theory", "recursion_theory", "type_theory", "category_theory"],
    "unknown_structure": ["graph_theory", "rewriting_systems", "modeling_first"],
}

DOMAIN_NOTES = {
    "graph_theory": ("ノード・辺・参照・分岐を扱う基本道具。", "構造の意味までは自動で与えない。"),
    "DAG": ("依存関係・履歴・証明順序を非循環構造で扱える。", "自己参照や循環を入れる場合は拡張が必要。"),
    "network_analysis": ("中心性・クラスタ・接続パターンを調べられる。", "数学的対象の定義には別層が必要。"),
    "universal_algebra": ("操作・入力スロット・出力を抽象的に扱える。", "抽象度が高く、最小例がないと空転しやすい。"),
    "semigroup_monoid_group": ("閉包・合成・単位元・逆の有無を段階的に検査できる。", "逆がない構造を無理に群にしない。"),
    "abstract_algebra": ("演算規則と不変量を調べる道具。", "対象集合と演算が未定義だと使えない。"),
    "category_theory": ("対象・写像・合成・図式で構造間の関係を扱える。", "初期モデルには重すぎる場合がある。"),
    "diagram_chasing": ("可換図式上の関係追跡に向く。", "写像と対象が明示されていないと使えない。"),
    "topology": ("局所/大域、連結性、穴、近傍を扱う。", "離散構造では位相の選び方が任意になりうる。"),
    "sheaf_theory": ("局所整合と大域貼り合わせの失敗を扱う。", "かなり高度。まず局所データと貼り合わせ規則が必要。"),
    "cohomology_style": ("局所的には整合するが大域的に破綻する現象の検出に向く発想。", "本格導入は重い。比喩利用から始める。"),
    "dynamical_systems": ("状態遷移・反復・収束・周期を扱う。", "状態空間と更新規則が必要。"),
    "automata_theory": ("離散状態と入力列による遷移を扱う。", "連続量や曖昧な状態は離散化が必要。"),
    "markov_process": ("確率的状態遷移を扱う。", "遷移確率を推定または仮定する必要がある。"),
    "cellular_automata": ("格子・近傍・局所更新規則に向く。", "局所規則を定義できないと使えない。"),
    "percolation_theory": ("格子上の連結・浸透・臨界現象を見る。", "行動や意味の説明には直結しない。"),
    "stochastic_process": ("確率的な時系列・点過程を扱う。", "分布仮定が必要になる。"),
    "order_theory": ("包含・精緻化・上位下位関係を扱える。", "演算的変化は別に定義する必要がある。"),
    "lattice_theory": ("合流・交差・上限下限を扱える。", "束条件が成立するか検査が必要。"),
    "logic": ("命題・規則・推論・矛盾を扱う。", "自然言語の意味を捨てる/固定する必要がある。"),
    "model_theory": ("構造とそれを満たす文の関係を見る。", "初期導入には重い。"),
    "SAT_CSP": ("制約充足・矛盾検出に向く。", "変数と制約の明示化が必要。"),
    "coding_theory": ("冗長性・誤り訂正・欠損耐性を扱う。", "意味より符号構造が対象。"),
    "information_theory": ("圧縮・情報量・ノイズ耐性を見る。", "構造の意味論は別扱い。"),
    "optimal_transport": ("質量・分布・コスト・流れの比較に向く。", "コスト関数が恣意的になりやすい。"),
    "network_flow": ("グラフ上の流量・容量・ボトルネックを見る。", "流れる量の定義が必要。"),
    "optimization": ("目的関数と制約のもとで最適解を探す。", "目的関数を勝手に置くと歪む。"),
    "rewriting_systems": ("規則による変形・生成・正規形を扱う。", "停止性・合流性を確認する必要がある。"),
    "formal_language": ("記号列・文法・生成規則を扱う。", "幾何や意味は別表現が必要。"),
    "computation_theory": ("計算可能性・生成過程・状態機械を扱う。", "実験データ分析には直接重い場合がある。"),
    "fixed_point_theory": ("反復して変わらない点・安定状態を見る。", "写像が明示されていないと使えない。"),
    "recursion_theory": ("自己参照・再帰的定義・計算可能性を見る。", "抽象度が高い。"),
    "type_theory": ("自己参照や構成規則を型で制御できる。", "導入コストが高い。"),
    "operad": ("複数入力・スロット・操作合成を扱う。", "かなり高度。直感だけで使うと破綻しやすい。"),
    "group_action": ("出力集合の対称性・入れ替え不変性を扱う。", "まず集合と作用が必要。"),
    "invariant_theory": ("変換しても変わらない量を探す。", "変換群の定義が必要。"),
    "combinatorics": ("有限構造・場合分け・配置を扱う。", "連続的変化や意味論は扱いにくい。"),
    "modeling_first": ("まだ分野確定せず、対象・操作・出力を先に固定する段階。", "数学分野の断定は保留する。"),
}

# =========================
# classifiers
# =========================

def normalize(t: str) -> str:
    return t.replace(" ", "").replace("　", "").replace("\n", "").replace("\r", "").strip()


def score_rule(t: str, keys: list[str]) -> int:
    return sum(1 for k in keys if k in t)


def classify_project(t: str) -> str:
    scores = {project: score_rule(t, keys) for project, keys in PROJECT_RULES.items()}
    best_project, best_score = max(scores.items(), key=lambda kv: kv[1])
    return best_project if best_score > 0 else "other"


def classify_layer(t: str, project: str | None = None) -> str:
    """
    layer:
      object = 内容としての対象
      tool   = 実装・操作としての対象
      meta   = 対象化そのもの・自己参照・層分離
    """
    if any(k in t for k in META_WORDS):
        return "meta"
    if any(k in t for k in TOOL_WORDS):
        return "tool"
    return "object"


def infer_op(t: str) -> str:
    # ERG*** の operation label に寄せる。
    if any(k in t for k in ["忘れ", "思い出", "今どうなった", "状態は", "状態"]):
        return "recall"
    if any(k in t for k in ["とは", "定義", "意味は", "何か", "なにか"]):
        return "define"
    if any(k in t for k in ["違い", "差", "比較", "どちら"]):
        return "compare"
    if any(k in t for k in ["なぜ", "理由", "導出", "derive"]):
        return "derive"
    if any(k in t for k in ["できる", "可能", "テスト", "確認", "レビュー", "正しい"]):
        return "test"
    if any(k in t for k in ["作って", "修正", "戻して", "やれ", "出せ", "実装", "追加", "生成"]):
        return "execute"
    if any(k in t for k in ["やめ", "凍結", "ここまで", "閉じ"]):
        return "close"
    if any(k in t for k in ["別", "方向", "シフト", "変える"]):
        return "shift"
    return "extend"


def infer_structure_scores(t: str) -> dict:
    return {name: score_rule(t, keys) for name, keys in STRUCTURE_RULES.items()}


def infer_structure(t: str) -> str:
    scores = infer_structure_scores(t)
    best, score = max(scores.items(), key=lambda kv: kv[1])
    return best if score > 0 else "unknown_structure"


def infer_structure_features(t: str) -> list:
    scores = infer_structure_scores(t)
    feats = [f"S:{name}" for name, score in scores.items() if score > 0]
    if not feats:
        feats = ["S:unknown_structure"]
    return sorted(feats)


def infer_domain_candidates(t: str, structure_override: str | None = None) -> list:
    scores = infer_structure_scores(t)
    if structure_override:
        scores[structure_override] = max(scores.get(structure_override, 0), 1)

    ranked_structures = sorted(
        [(score, name) for name, score in scores.items() if score > 0],
        key=lambda x: (x[0], x[1]),
        reverse=True,
    )
    if not ranked_structures:
        ranked_structures = [(1, "unknown_structure")]

    domain_score = {}
    for rank_weight, structure in ranked_structures:
        for i, domain in enumerate(DOMAIN_BY_STRUCTURE.get(structure, [])):
            domain_score[domain] = domain_score.get(domain, 0) + rank_weight * 10 - i

    ranked_domains = sorted(domain_score.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    return [d for d, _ in ranked_domains[:8]]


def extract_features(t: str):
    f = set()

    for k in KEYWORDS:
        if k in t:
            f.add("c:" + k)

    # unresolved / task flags
    if any(k in t for k in ["どうなった", "状態", "現状", "今"]):
        f.add("U:status")
    if any(k in t for k in ["違い", "差", "差分", "比較"]):
        f.add("U:diff")
    if any(k in t for k in ["意味", "とは", "何か", "なにか"]):
        f.add("U:meaning")
    if any(k in t for k in ["どうすれば", "手順", "作業", "実装", "構成", "パイプライン"]):
        f.add("U:procedure")
    if any(k in t for k in ["自己参照", "ERGでERG", "層", "layer", "メタ", "混線", "ループ"]):
        f.add("U:meta")
    if any(k in t for k in ["どの分野", "分野", "道具", "数学的構造", "数学の道具", "ルータ", "router"]):
        f.add("U:domain_route")

    op = infer_op(t)
    project = classify_project(t)
    layer = classify_layer(t, project)
    structure = infer_structure(t)
    domains = infer_domain_candidates(t, structure)

    f.add("op:" + op)
    f.add("project:" + project)
    f.add("layer:" + layer)
    f.add("structure:" + structure)
    for sf in infer_structure_features(t):
        f.add(sf)
    for d in domains[:5]:
        f.add("domain:" + d)
    return f

# =========================
# IO
# =========================

NODE_KEYS = {f.name for f in fields(Node)}
EDGE_KEYS = {f.name for f in fields(Edge)}


def read_jsonl(path: Path):
    if not path.exists():
        return []
    items = []
    with open(path, encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            if not line.strip():
                continue
            try:
                items.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"skip invalid json: {path.name}:{line_no}: {e}")
    return items


def node_from_dict(d: dict) -> Node:
    # 古いJSONLとの互換用。余分なkeyは無視し、欠けたkeyは補う。
    base = {k: d[k] for k in d.keys() & NODE_KEYS}
    text = base.get("text", d.get("text", ""))
    project = base.get("project", classify_project(text))
    layer = base.get("layer", classify_layer(text, project))
    structure = base.get("structure", infer_structure(text))
    structure_features = base.get("structure_features", infer_structure_features(text))
    domain_candidates = base.get("domain_candidates", infer_domain_candidates(text, structure))

    base.setdefault("id", "m_??????")
    base.setdefault("timestamp", datetime.now(JST).isoformat(timespec="seconds"))
    base.setdefault("project", project)
    base.setdefault("layer", layer)
    base.setdefault("structure", structure)
    base.setdefault("text", text)
    base.setdefault("op", infer_op(base["text"]))
    base.setdefault("features", sorted(extract_features(base["text"])))
    base.setdefault("sigma", list(base["features"]))
    base.setdefault("structure_features", structure_features)
    base.setdefault("domain_candidates", domain_candidates)
    base.setdefault("recency", 3)
    base.setdefault("branch_degree", 0)
    base.setdefault("locked", False)
    base.setdefault("source", "")
    return Node(**base)


def edge_from_dict(d: dict) -> Edge:
    base = {k: d[k] for k in d.keys() & EDGE_KEYS}
    base.setdefault("source", "")
    base.setdefault("target", "")
    base.setdefault("type", "unknown")
    return Edge(**base)


def load_nodes():
    return [node_from_dict(d) for d in read_jsonl(NODES)]


def load_edges():
    return [edge_from_dict(d) for d in read_jsonl(EDGES)]


def save_nodes(nodes):
    with open(NODES, "w", encoding="utf-8") as f:
        for n in nodes:
            f.write(json.dumps(asdict(n), ensure_ascii=False) + "\n")


def save_edges(edges):
    with open(EDGES, "w", encoding="utf-8") as f:
        for e in edges:
            f.write(json.dumps(asdict(e), ensure_ascii=False) + "\n")


def append_node(node):
    with open(NODES, "a", encoding="utf-8") as f:
        f.write(json.dumps(asdict(node), ensure_ascii=False) + "\n")


def append_edge(edge):
    with open(EDGES, "a", encoding="utf-8") as f:
        f.write(json.dumps(asdict(edge), ensure_ascii=False) + "\n")

# =========================
# core helpers
# =========================


def recency(ts: str) -> int:
    now = datetime.now(JST)
    try:
        t = datetime.fromisoformat(ts)
    except ValueError:
        return 0
    d = now - t
    if d <= timedelta(days=7):
        return 3
    if d <= timedelta(days=30):
        return 2
    if d <= timedelta(days=180):
        return 1
    return 0


def allowed_project(qp: str, np: str) -> bool:
    if qp == np:
        return True
    # ERG/HVM/GIF/DIFは構造探索層として相互参照を許可。
    structural = {"ERG", "GIF", "DIF", "math"}
    if qp in structural and np in structural:
        return True
    if qp == "ERG" and np in {"CPR", "coding"}:
        return True
    if qp == "CPR" and np in {"ERG", "coding", "math"}:
        return True
    if qp == "coding" and np in {"ERG", "CPR", "GIF", "DIF", "math"}:
        return True
    if qp == "other" and np in structural:
        return True
    return False


def layer_relation(q_layer: str, n_layer: str) -> int:
    """
    3 = exact
    2 = meta query が object/tool を対象化する
    1 = 補助文脈として許可
    0 = 原則低優先
    """
    if q_layer == n_layer:
        return 3
    if q_layer == "meta" and n_layer in {"object", "tool"}:
        return 2
    if q_layer == "tool" and n_layer in {"object", "meta"}:
        return 1
    if q_layer == "object" and n_layer == "tool":
        return 1
    return 0


def structure_relation(q_structure: str, n_structure: str, q_domains: list, n_domains: list) -> int:
    if q_structure == n_structure:
        return 3
    if set(q_domains) & set(n_domains):
        return 2
    if q_structure == "unknown_structure" or n_structure == "unknown_structure":
        return 1
    return 0


def compute_sigma(nodes, i: int, window: int = 3):
    """
    sigma = その発話の局所特徴 + 直近同project同layer文脈 + 同structure文脈。
    全履歴累積をやめ、project/layer混線を抑えつつ、数学構造探索の再接続を許す。
    """
    cur = nodes[i]
    sig = set(cur.features)
    count = 0
    for j in range(i - 1, -1, -1):
        same_project_layer = nodes[j].project == cur.project and nodes[j].layer == cur.layer
        same_structure = nodes[j].structure == cur.structure and cur.structure != "unknown_structure"
        if same_project_layer or same_structure:
            sig |= set(nodes[j].features)
            count += 1
        if count >= window:
            break
    return sorted(sig)


def make_node(text: str, agent_project=None, agent_layer=None, agent_structure=None) -> Node:
    nodes = load_nodes()
    nid = f"m_{len(nodes):06d}"
    ts = datetime.now(JST).isoformat(timespec="seconds")
    proj = agent_project or classify_project(text)
    layer = agent_layer or classify_layer(text, proj)
    structure = agent_structure or infer_structure(text)
    op = infer_op(text)
    structure_features = infer_structure_features(text)
    domain_candidates = infer_domain_candidates(text, structure)
    feat = sorted(extract_features(text))
    node = Node(
        id=nid,
        timestamp=ts,
        project=proj,
        layer=layer,
        structure=structure,
        text=text,
        op=op,
        features=feat,
        sigma=feat,
        structure_features=structure_features,
        domain_candidates=domain_candidates,
        recency=3,
        branch_degree=0,
        locked=False,
        source="",
    )
    return node


# =========================
# maintenance helpers: import/export/dedupe/prune
# =========================

def resolve_local_path(path_text: str) -> Path:
    """Resolve a path relative to current folder, then BASE_DIR."""
    p = Path(path_text).expanduser()
    if p.is_absolute():
        return p
    if p.exists():
        return p.resolve()
    return (BASE_DIR / path_text).resolve()


def renumber_nodes(nodes):
    """Keep node ids contiguous after prune/dedupe so future ids do not collide."""
    for i, n in enumerate(nodes):
        n.id = f"m_{i:06d}"
    return nodes


def refresh_node_fields(n: Node):
    """
    Recompute derived fields.
    If n.locked=True, preserve project/layer/structure/op supplied by seed import.
    """
    if not getattr(n, "locked", False):
        n.project = classify_project(n.text)
        n.layer = classify_layer(n.text, n.project)
        n.structure = infer_structure(n.text)
        n.op = infer_op(n.text)

    n.structure_features = infer_structure_features(n.text)
    # locked node may have manual structure; route domains from that structure.
    n.domain_candidates = infer_domain_candidates(n.text, n.structure)
    feats = set(extract_features(n.text))
    feats.add("project:" + n.project)
    feats.add("layer:" + n.layer)
    feats.add("structure:" + n.structure)
    for d in n.domain_candidates[:5]:
        feats.add("domain:" + d)
    if getattr(n, "source", ""):
        feats.add("source:" + n.source)
    if getattr(n, "locked", False):
        feats.add("locked:true")
    n.features = sorted(feats)
    n.recency = recency(n.timestamp)
    n.branch_degree = 0
    return n


def seed_record_to_node(record: dict, nid: str) -> Node | None:
    text = str(record.get("text", "")).strip()
    if not text:
        return None
    project = record.get("project") or classify_project(text)
    layer = record.get("layer") or classify_layer(text, project)
    structure = record.get("structure") or infer_structure(text)
    op = record.get("op") or infer_op(text)
    ts = record.get("timestamp") or datetime.now(JST).isoformat(timespec="seconds")
    locked = bool(record.get("locked", True))
    source = record.get("source", "seed_import")
    domains = record.get("domain_candidates") or infer_domain_candidates(text, structure)
    structure_features = record.get("structure_features") or infer_structure_features(text)
    feats = set(extract_features(text))
    feats |= {"project:" + project, "layer:" + layer, "structure:" + structure}
    for d in domains[:5]:
        feats.add("domain:" + d)
    feats.add("source:" + source)
    if locked:
        feats.add("locked:true")
    return Node(
        id=nid,
        timestamp=ts,
        project=project,
        layer=layer,
        structure=structure,
        text=text,
        op=op,
        features=sorted(feats),
        sigma=sorted(feats),
        structure_features=structure_features,
        domain_candidates=domains,
        recency=3,
        branch_degree=0,
        locked=locked,
        source=source,
    )


def read_seed_records(path: Path):
    records = []
    with open(path, encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                obj = json.loads(line)
                if isinstance(obj, dict):
                    records.append(obj)
                else:
                    print(f"skip non-object json: {path.name}:{line_no}")
            except json.JSONDecodeError:
                # Plain text line fallback.
                records.append({"text": line})
    return records


def import_seed(path_text: str):
    path = resolve_local_path(path_text)
    if not path.exists():
        print("import file not found:", path)
        return
    nodes = load_nodes()
    seen = {normalize(n.text) for n in nodes}
    records = read_seed_records(path)
    added = 0
    skipped = 0
    for rec in records:
        text = str(rec.get("text", "")).strip()
        if not text:
            skipped += 1
            continue
        key = normalize(text)
        if key in seen:
            skipped += 1
            continue
        node = seed_record_to_node(rec, f"m_{len(nodes):06d}")
        if node is None:
            skipped += 1
            continue
        nodes.append(node)
        seen.add(key)
        added += 1
    save_nodes(nodes)
    rebuild()
    print("import done:", path)
    print("added:", added, "skipped:", skipped)


def export_seed(path_text: str):
    path = resolve_local_path(path_text or "seed_export.jsonl")
    nodes = load_nodes()
    with open(path, "w", encoding="utf-8") as f:
        for n in nodes:
            rec = {
                "text": n.text,
                "project": n.project,
                "layer": n.layer,
                "structure": n.structure,
                "op": n.op,
                "domain_candidates": n.domain_candidates,
                "locked": getattr(n, "locked", False),
                "source": getattr(n, "source", ""),
            }
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print("export done:", path)
    print("nodes:", len(nodes))


def dedupe():
    nodes = load_nodes()
    seen = set()
    kept = []
    removed = []
    for n in nodes:
        key = normalize(n.text)
        if key in seen:
            removed.append(n)
            continue
        seen.add(key)
        kept.append(n)
    renumber_nodes(kept)
    save_nodes(kept)
    rebuild()
    print("dedupe done")
    print("kept:", len(kept), "removed:", len(removed))
    if removed:
        print("removed ids:", ", ".join(n.id for n in removed[:20]))


def prune_last(count_text: str):
    try:
        count = int(count_text)
    except ValueError:
        print("usage: python memory_erg_app.py prune N")
        return
    if count <= 0:
        print("N must be positive")
        return
    nodes = load_nodes()
    if count > len(nodes):
        count = len(nodes)
    removed = nodes[-count:]
    kept = nodes[:-count]
    renumber_nodes(kept)
    save_nodes(kept)
    rebuild()
    print("prune done")
    print("removed:", len(removed))
    for n in removed:
        print("-", n.id, n.project, n.layer, n.structure, n.text[:80])

# =========================
# command arg helpers
# =========================


def parse_optional_args(args, default_model="llama3.1"):
    """--model, --layer, --structure, --limit を抜き取り、残りを本文として返す。"""
    args = list(args)
    model = default_model
    layer = None
    structure = None
    limit = 8

    def pop_value(flag):
        nonlocal args
        if flag not in args:
            return None
        k = args.index(flag)
        if k + 1 >= len(args):
            raise ValueError(f"value required after {flag}")
        value = args[k + 1]
        del args[k:k + 2]
        return value

    v = pop_value("--model")
    if v is not None:
        model = v

    v = pop_value("--layer")
    if v is not None:
        if v not in {"object", "tool", "meta"}:
            raise ValueError("--layer must be object / tool / meta")
        layer = v

    v = pop_value("--structure")
    if v is not None:
        if v not in set(STRUCTURE_RULES) | {"unknown_structure"}:
            raise ValueError("unknown --structure value")
        structure = v

    v = pop_value("--limit")
    if v is not None:
        try:
            limit = int(v)
        except ValueError:
            raise ValueError("--limit must be integer")

    text = " ".join(args).strip()
    return text, model, layer, structure, limit

# =========================
# commands: add / rebuild / query / layer / route
# =========================


def add(text: str, layer_override=None, structure_override=None):
    nodes = load_nodes()
    text_norm = normalize(text)

    for n in nodes:
        if normalize(n.text) == text_norm:
            print("skip duplicate:", n.id)
            return

    node = make_node(text, agent_layer=layer_override, agent_structure=structure_override)
    append_node(node)

    if nodes:
        append_edge(Edge(nodes[-1].id, node.id, "extends_main"))

    print("added:", node.id, node.project, node.layer, node.structure, node.op)


def rebuild():
    nodes = load_nodes()
    edges = []

    # derived fieldsを再計算。locked=True の seed node は手動指定を保持する。
    for n in nodes:
        refresh_node_fields(n)

    # sigmaを局所文脈として再計算
    for i in range(len(nodes)):
        nodes[i].sigma = compute_sigma(nodes, i)

    # main edges
    for i in range(1, len(nodes)):
        edges.append(Edge(nodes[i - 1].id, nodes[i].id, "extends_main"))

    # branch edges: project/layer/structure/featuresが重なる過去ノードへ張る
    for i in range(len(nodes)):
        cur = nodes[i]
        cur_f = set(cur.features)
        cand = []
        for j in range(0, i - 1):
            prev = nodes[j]
            if not allowed_project(cur.project, prev.project):
                continue
            prev_f = set(prev.features)
            sim = len(cur_f & prev_f)
            rel_structure = structure_relation(cur.structure, prev.structure, cur.domain_candidates, prev.domain_candidates)
            if sim == 0 and rel_structure == 0:
                continue
            same_project = int(cur.project == prev.project)
            rel_layer = layer_relation(cur.layer, prev.layer)
            distance = i - j
            score = (rel_structure, sim, same_project, rel_layer, prev.recency, -distance, j)
            cand.append((score, j))

        cand.sort(key=lambda x: x[0], reverse=True)
        for _, j in cand[:2]:
            edges.append(Edge(nodes[j].id, cur.id, "extends_branch"))

    # branch_degree = outgoing branch count
    deg = {n.id: 0 for n in nodes}
    for e in edges:
        if e.type == "extends_branch":
            deg[e.source] += 1

    for n in nodes:
        n.branch_degree = deg[n.id]

    save_nodes(nodes)
    save_edges(edges)
    print("rebuild done")
    print("nodes:", len(nodes), "edges:", len(edges))


def select_nodes(q: str, limit: int = 8, layer_override=None, structure_override=None):
    nodes = load_nodes()
    qp = classify_project(q)
    q_layer = layer_override or classify_layer(q, qp)
    q_structure = structure_override or infer_structure(q)
    q_domains = infer_domain_candidates(q, q_structure)
    qf = extract_features(q)

    cand = []
    for n in nodes:
        if not allowed_project(qp, n.project):
            continue

        nf = set(n.features)
        ns = set(n.sigma)
        ov_local = len(qf & nf)
        ov_sigma = len(qf & ns)
        rel_layer = layer_relation(q_layer, n.layer)
        rel_structure = structure_relation(q_structure, n.structure, q_domains, n.domain_candidates)
        domain_overlap = len(set(q_domains) & set(n.domain_candidates))

        if ov_local == 0 and ov_sigma == 0 and rel_structure == 0 and domain_overlap == 0:
            continue
        if rel_layer == 0 and ov_local < 2 and rel_structure < 2:
            continue
        if n.recency == 0 and ov_local < 2 and rel_structure < 2:
            continue

        score = (
            int(n.project == qp),
            rel_structure,
            domain_overlap,
            rel_layer,
            ov_local,
            ov_sigma,
            n.recency,
            min(n.branch_degree, 3),
            n.id,
        )
        cand.append((score, n))

    cand.sort(key=lambda x: x[0], reverse=True)
    return [n for _, n in cand[:limit]]


def query(q: str, layer_override=None, structure_override=None, limit: int = 8):
    sel = select_nodes(q, layer_override=layer_override, structure_override=structure_override, limit=limit)
    print("---- result ----")
    for n in sel:
        domains = ",".join(n.domain_candidates[:3])
        print(n.id, n.project, n.layer, n.structure, n.op, f"domains=[{domains}]", n.text)


def show_layer(text: str):
    project = classify_project(text)
    layer = classify_layer(text, project)
    structure = infer_structure(text)
    domains = infer_domain_candidates(text, structure)
    op = infer_op(text)
    print("project:", project)
    print("layer:", layer)
    print("structure:", structure)
    print("domain_candidates:", ", ".join(domains))
    print("operation:", op)
    print("features:", ", ".join(sorted(extract_features(text))))

# =========================
# Math Domain Router
# =========================


def domain_candidate_lines(domains: list) -> str:
    if not domains:
        return "(none)"
    lines = []
    for i, d in enumerate(domains, start=1):
        reason, risk = DOMAIN_NOTES.get(d, ("候補分野。", "未定義。"))
        lines.append(f"{i}. {d}\n   reason: {reason}\n   risk: {risk}")
    return "\n".join(lines)


def build_router_report(text: str, structure_override=None) -> str:
    project = classify_project(text)
    layer = classify_layer(text, project)
    structure = structure_override or infer_structure(text)
    structure_features = infer_structure_features(text)
    domains = infer_domain_candidates(text, structure)

    return f"""[STRUCTURE_INPUT]
{text}

[ROUTED_PROJECT]
{project}

[ROUTED_LAYER]
{layer}

[ROUTED_STRUCTURE]
{structure}

[STRUCTURE_FEATURES]
""" + "\n".join(structure_features) + f"""

[DOMAIN_CANDIDATES]
{domain_candidate_lines(domains)}

[REQUIRED_NEXT_TEST]
- 対象集合を1つ固定する。
- 操作または遷移を1つ明示する。
- 最小例を3〜5個だけ列挙する。
- 失敗例を1つ作る。
- 候補分野を断定せず、どの定義が必要かを確認する。
"""


def route(text: str, structure_override=None):
    print(build_router_report(text, structure_override=structure_override))

# =========================
# HVM packet
# =========================


def format_trace(nodes):
    if not nodes:
        return "(no relevant nodes)"
    ordered = sorted(nodes, key=lambda n: n.id)
    return "\n".join(
        f"{n.id} {n.project}/{n.layer}/{n.structure} {n.op} {n.text}"
        for n in ordered
    )


def format_layered_trace(nodes):
    if not nodes:
        return "(no relevant nodes)"
    ordered = sorted(nodes, key=lambda n: n.id)
    blocks = []
    for layer in ["object", "tool", "meta"]:
        lines = [
            f"{n.id} {n.project}/{n.layer}/{n.structure} {n.op} {n.text}"
            for n in ordered if n.layer == layer
        ]
        if lines:
            blocks.append(f"[{layer}]\n" + "\n".join(lines))
    return "\n\n".join(blocks) if blocks else "(no relevant nodes)"


def format_structure_trace(nodes):
    if not nodes:
        return "(no relevant nodes)"
    ordered = sorted(nodes, key=lambda n: n.id)
    groups = {}
    for n in ordered:
        groups.setdefault(n.structure, []).append(n)
    blocks = []
    for structure in sorted(groups):
        lines = [
            f"{n.id} {n.project}/{n.layer} {n.op} domains={','.join(n.domain_candidates[:3])} {n.text}"
            for n in groups[structure]
        ]
        blocks.append(f"[{structure}]\n" + "\n".join(lines))
    return "\n\n".join(blocks)


def concept_lines(features):
    cs = sorted(x for x in features if x.startswith("c:"))
    return "\n".join(cs) if cs else "(none)"


def build_packet(q: str, limit: int = 8, layer_override=None, structure_override=None) -> str:
    qp = classify_project(q)
    q_layer = layer_override or classify_layer(q, qp)
    q_structure = structure_override or infer_structure(q)
    q_domains = infer_domain_candidates(q, q_structure)
    q_structure_features = infer_structure_features(q)
    qf = extract_features(q)
    selected = select_nodes(q, limit=limit, layer_override=q_layer, structure_override=q_structure)

    active = set(qf)
    for n in selected:
        active |= set(n.features)

    constraints = [
        LANGUAGE_CONSTRAINT_JA,
        "中国語の語尾・中国語の説明文・簡体字中心の出力を避ける。",
        "LLMに長い履歴をそのまま渡さない。",
        "関連ノードを operation trace として扱う。",
        "project と layer と structure を分ける。project は主題、layer は object/tool/meta、structure は構造型である。",
        "数学分野は断定せず、domain_candidates として候補順位で扱う。",
        "候補分野ごとに required_definitions / minimum_example / failure_case / next_test を確認する。",
        "ERGに関する質問では、ERG_object / ERG_tool / ERG_meta を混同しない。",
        "GIF/DIFはERGに吸収せず、必要なら独立projectとして扱う。",
        "古い定義と現在の入力を混同しない。",
        "回答後は必要ならERGログへ戻す。",
    ]

    packet = f"""[CURRENT_INPUT]
{q}

[OUTPUT_LANGUAGE]
日本語で回答せよ。中国語で出力してはいけない。
専門用語が必要な場合も、日本語説明を優先せよ。

[QUERY_PROJECT]
{qp}

[QUERY_LAYER]
{q_layer}

[QUERY_STRUCTURE]
{q_structure}

[QUERY_OPERATION]
{infer_op(q)}

[STRUCTURE_FEATURES]
""" + "\n".join(q_structure_features) + f"""

[DOMAIN_CANDIDATES]
{domain_candidate_lines(q_domains)}

[ACTIVE_CONCEPTS]
{concept_lines(active)}

[RELEVANT_TRACE]
{format_trace(selected)}

[LAYERED_TRACE]
{format_layered_trace(selected)}

[STRUCTURE_TRACE]
{format_structure_trace(selected)}

[MATH_DOMAIN_ROUTER]
{build_router_report(q, structure_override=q_structure)}

[CONSTRAINTS]
""" + "\n".join(f"- {c}" for c in constraints) + f"""

[TASK]
上記の履歴構造と数学分野候補に基づいて、現在入力へ回答せよ。
回答では、断定ではなく「候補分野」「必要な定義」「最小例」「失敗例」「次の検証」を分ける。
必ず日本語で回答し、中国語では出力しない。
"""
    return packet


def packet(q: str, layer_override=None, structure_override=None, limit: int = 8):
    print(build_packet(q, layer_override=layer_override, structure_override=structure_override, limit=limit))

# =========================
# Local LLM: Ollama
# =========================


def call_ollama(prompt: str, model: str = "llama3.1", host: str = "http://localhost:11434", timeout: int = 600) -> str:
    url = host.rstrip("/") + "/api/generate"
    payload = json.dumps({
        "model": model,
        "system": SYSTEM_PROMPT_JA,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.2},
    }, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as res:
        data = json.loads(res.read().decode("utf-8"))
    return data.get("response", "")


def ask(q: str, model: str = "llama3.1", layer_override=None, structure_override=None, limit: int = 8):
    # 現在入力そのものが検索結果に混ざらないよう、先にpacketを作る。
    # 失敗した入力でERGログを汚さないよう、Ollama応答成功後に user/assistant node を保存する。
    qp = classify_project(q)
    q_layer = layer_override or classify_layer(q, qp)
    q_structure = structure_override or infer_structure(q)
    p = build_packet(q, layer_override=q_layer, structure_override=q_structure, limit=limit)

    try:
        answer = call_ollama(p, model=model)
    except urllib.error.HTTPError as e:
        print("Ollama connection failed.")
        print("model:", model)
        print("error:", e)
        if e.code == 404:
            print("原因候補: そのモデルがOllamaに入っていません。PowerShellで `ollama list` を確認し、必要なら `ollama pull " + model + "` を実行してください。")
        try:
            print("detail:", e.read().decode("utf-8", errors="replace"))
        except Exception:
            pass
        print("\n---- HVM PACKET ----")
        print(p)
        return
    except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
        print("Ollama connection failed.")
        print("model:", model)
        print("error:", e)
        print("対処: Ollamaが起動しているか、モデルが重すぎないかを確認してください。")
        print("\n---- HVM PACKET ----")
        print(p)
        return

    print(answer)

    # 成功後に user node / assistant node を保存
    before = load_nodes()
    user_node = make_node(q, agent_layer=q_layer, agent_structure=q_structure)
    append_node(user_node)
    if before:
        append_edge(Edge(before[-1].id, user_node.id, "extends_main"))

    assistant_node = make_node(answer, agent_project=qp, agent_layer=q_layer, agent_structure=q_structure)
    assistant_node.op = "extend"
    assistant_node.features = sorted(
        extract_features(answer) | extract_features(q) |
        {"layer:" + q_layer, "project:" + qp, "structure:" + q_structure} |
        {"domain:" + d for d in infer_domain_candidates(q, q_structure)[:5]}
    )
    assistant_node.sigma = assistant_node.features
    append_node(assistant_node)
    append_edge(Edge(user_node.id, assistant_node.id, "reply"))


def status():
    nodes = load_nodes()
    edges = load_edges()
    by_project = {}
    by_layer = {}
    by_structure = {}
    by_project_layer = {}
    by_op = {}
    domains = {}
    by_source = {}
    locked_count = 0
    for n in nodes:
        by_project[n.project] = by_project.get(n.project, 0) + 1
        by_layer[n.layer] = by_layer.get(n.layer, 0) + 1
        by_structure[n.structure] = by_structure.get(n.structure, 0) + 1
        key = f"{n.project}/{n.layer}"
        by_project_layer[key] = by_project_layer.get(key, 0) + 1
        by_op[n.op] = by_op.get(n.op, 0) + 1
        for d in n.domain_candidates[:3]:
            domains[d] = domains.get(d, 0) + 1
        src = getattr(n, "source", "") or "normal"
        by_source[src] = by_source.get(src, 0) + 1
        if getattr(n, "locked", False):
            locked_count += 1
    print("STORE:", STORE)
    print("nodes:", len(nodes))
    print("edges:", len(edges))
    print("projects:", by_project)
    print("layers:", by_layer)
    print("structures:", by_structure)
    print("project/layer:", by_project_layer)
    print("operations:", by_op)
    print("top domains:", dict(sorted(domains.items(), key=lambda kv: kv[1], reverse=True)[:12]))
    print("sources:", by_source)
    print("locked:", locked_count)


# =========================
# GitHub / dual-agent math protocol helpers
# =========================

ROLE_ALIASES = {
    "gpt": "proposer",
    "free": "proposer",
    "proposer": "proposer",
    "idea": "proposer",
    "codex": "critic",
    "reviewer": "critic",
    "critic": "critic",
    "skeptic": "critic",
    "synth": "synthesizer",
    "synthesizer": "synthesizer",
    "judge": "synthesizer",
}

ROLE_SPECS = {
    "proposer": {
        "name": "自由発想役",
        "mission": "ERGの数学的トイモデル候補を広げる。新しい定義、最小例、操作、可視化、実装方針を提案する。",
        "must": [
            "提案を Claim / Definition / Operation / Example に分ける。",
            "まだ合意されていない内容は accepted と書かず、proposal と書く。",
            "最小例を1つ以上置く。",
            "既存の accepted kernel を壊す場合は、その理由を明示する。",
        ],
        "avoid": [
            "巨大な理論体系へ一気に飛ぶこと。",
            "圏論・層・不動点などの名前だけで説明を終えること。",
            "未検証の比喩を定義として固定すること。",
        ],
    },
    "critic": {
        "name": "検証・反証役",
        "mission": "自由発想役の提案を、定義の型、循環、曖昧さ、反例、実装可能性、git差分としての追跡可能性から検査する。",
        "must": [
            "各Claimに対して accept / reject / needs_test / split を付ける。",
            "曖昧な語を required_definition として列挙する。",
            "最小反例または失敗例を1つ以上作る。",
            "READMEに昇格できる内容と、proposalに留める内容を分ける。",
        ],
        "avoid": [
            "単に保守的に却下すること。",
            "実装細部だけを見て数学的定義の不備を見逃すこと。",
            "自然言語の印象批評で終えること。",
        ],
    },
    "synthesizer": {
        "name": "合意形成役",
        "mission": "提案と検証を統合し、README / FORMALIZATION / CONVERGENCE / issue に反映すべき差分へ変換する。",
        "must": [
            "accepted / rejected / postponed / open_question を分ける。",
            "READMEへ昇格する1〜3個の安定命題だけを選ぶ。",
            "次ラウンドの検証課題を最大3個に絞る。",
            "git commit message 案を出す。",
        ],
        "avoid": [
            "全部を採用すること。",
            "未確定事項をREADMEの中心定義に混ぜること。",
            "会話ログと合意ログを混同すること。",
        ],
    },
}


def slugify_for_file(text: str, fallback: str = "round") -> str:
    allowed = []
    for ch in text.strip():
        if ch.isalnum() or ch in {"-", "_"}:
            allowed.append(ch)
        elif ch in {" ", "　", "/", "\\", ":", "|"}:
            allowed.append("-")
    slug = "".join(allowed).strip("-_")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug[:80] or fallback


def parse_role_and_text(raw: str):
    parts = raw.strip().split(maxsplit=1)
    if not parts:
        raise ValueError("role and text required")
    role = ROLE_ALIASES.get(parts[0].lower())
    if role is None:
        raise ValueError("role must be one of: " + ", ".join(sorted(ROLE_ALIASES)))
    if len(parts) < 2 or not parts[1].strip():
        raise ValueError("text required after role")
    return role, parts[1].strip()


def role_instruction_block(role: str) -> str:
    spec = ROLE_SPECS[role]
    lines = [
        f"[ROLE]",
        f"{role}: {spec['name']}",
        "",
        "[MISSION]",
        spec["mission"],
        "",
        "[MUST]",
    ]
    lines.extend(f"- {x}" for x in spec["must"])
    lines.append("")
    lines.append("[AVOID]")
    lines.extend(f"- {x}" for x in spec["avoid"])
    return "\n".join(lines)


def build_role_packet(role: str, q: str, limit: int = 8, layer_override=None, structure_override=None) -> str:
    base = build_packet(q, limit=limit, layer_override=layer_override, structure_override=structure_override)
    schema = """[DUAL_AGENT_PROTOCOL]
- GPT/proposer は proposal を増やす。
- Codex/critic は proposal を検査し、accept / reject / needs_test / split を返す。
- synthesizer は accepted kernel と open questions に分離する。
- GitHub上では README.md を安定合意、docs/FORMALIZATION.md を数学的定義、docs/CONVERGENCE.md を収束指標、logs/ を往復ログ、decisions/ を合意決定として使う。
- READMEへ昇格できるのは、critic の検査を通り、最小例と失敗例がある命題だけである。

[OUTPUT_SCHEMA]
## 1. Verdict
accept / reject / needs_test / split / proposal のいずれか。

## 2. Atomic claims
C001:
  status:
  statement:
  type: definition / theorem_candidate / operation / example / implementation / question
  depends_on:
  risk:

## 3. Required definitions
D?:
  term:
  missing point:
  proposed definition:

## 4. Minimum examples
E?:
  object:
  operation:
  expected result:

## 5. Failure cases
F?:
  object:
  why it breaks:

## 6. GitHub diff target
README.md:
docs/FORMALIZATION.md:
docs/CONVERGENCE.md:
logs/:
decisions/:

## 7. Next round prompt
次に相手役へ渡す短いプロンプト。
"""
    return role_instruction_block(role) + "\n\n" + schema + "\n\n" + base


def role_packet(raw: str, layer_override=None, structure_override=None, limit: int = 8):
    try:
        role, q = parse_role_and_text(raw)
    except ValueError as e:
        print("argument error:", e)
        print("usage: python memory_erg_app.py role_packet proposer|critic|synthesizer \"text\"")
        return
    print(build_role_packet(role, q, limit=limit, layer_override=layer_override, structure_override=structure_override))


SCAFFOLD_FILES = {
    "README.md": """# ERG-TAO Math Toy Model

このリポジトリは、ERG（Explicit Relational Graph）を数学的トイモデルとして固めるための外部ログである。

## Current accepted kernel

現時点の最小核は次の通り。

1. ERG is treated as a typed directed multigraph.
2. Nodes represent artifacts such as messages, propositions, definitions, examples, operations, files, commits, and decisions.
3. Edges represent typed relations such as `refines`, `rejects`, `depends_on`, `contradicts`, `implements`, `logs`, and `supersedes`.
4. A claim is not accepted merely because it appears in conversation.
5. A claim becomes stable only when it is represented in `docs/FORMALIZATION.md`, checked by a critic role, and reflected in `docs/CONVERGENCE.md`.

## Repository roles

- `README.md`: stable public-facing summary.
- `docs/FORMALIZATION.md`: current mathematical formalization.
- `docs/CONVERGENCE.md`: convergence criteria and observed changes.
- `logs/`: GPT/Codex round logs.
- `decisions/`: accepted decisions.
- `proposals/`: unaccepted proposals.
- `erg_store/`: optional generated JSONL graph data.

## Working rule

README is not a scratchpad.
Unstable ideas go to `proposals/` or `logs/`.
Accepted definitions are promoted only after review.

""",
    "docs/FORMALIZATION.md": """# Formalization

## Version

v0.1 toy model.

## Basic objects

Let

```text
G = (V, E, type_V, type_E, attr)
```

where:

- `V` is a finite set of nodes.
- `E` is a finite set of directed typed edges.
- `type_V: V -> NodeType`.
- `type_E: E -> EdgeType`.
- `attr` assigns metadata to nodes and edges.

## Node types

Initial node types:

```text
Message
Proposal
Claim
Definition
Operation
Example
FailureCase
File
Commit
Decision
OpenQuestion
```

## Edge types

Initial edge types:

```text
mentions
proposes
refines
rejects
depends_on
contradicts
implements
logs
supersedes
accepted_as
needs_test
```

## Acceptance rule

A claim `c` may be marked `accepted_as` only if:

1. `c` has a written definition.
2. `c` has at least one minimum example.
3. `c` has at least one failure case or boundary case.
4. `c` has been reviewed by the critic role.
5. `c` is reflected in the convergence log.

## Open issues

- Whether ERG should remain a directed multigraph or become a DAG at the accepted layer.
- How to represent cycles without destroying the acyclic proof/history layer.
- Whether git commits should be first-class nodes or only source metadata.
- How to define convergence quantitatively.

""",
    "docs/CONVERGENCE.md": """# Convergence Log

## Definition of convergence

A topic is considered more converged when:

1. accepted definitions change less frequently;
2. open questions decrease or become more precise;
3. rejected alternatives are explicitly recorded;
4. examples and failure cases stop changing the core definition;
5. README diffs become smaller while FORMALIZATION becomes sharper.

## Suggested measurable indicators

```text
accepted_claim_count
open_question_count
rejected_claim_count
definition_churn_lines
readme_churn_lines
formalization_churn_lines
rounds_since_last_kernel_change
```

## Round table

| Round | Date | Topic | Accepted | Rejected | Open | README changed | Formalization changed |
|---|---|---|---:|---:|---:|---|---|
| R000 | YYYY-MM-DD | initialize toy model | 5 | 0 | 4 | yes | yes |

""",
    "logs/README.md": """# Round Logs

Each round should preserve the role, prompt, answer, accepted claims, rejected claims, and next prompt.

Recommended filename:

```text
YYYYMMDD-HHMM-role-topic.md
```

""",
    "proposals/README.md": """# Proposals

Unaccepted ideas go here first.
Do not move them into README until critic review and synthesis are complete.

""",
    "decisions/ADR-0001-use-git-as-external-erg-log.md": """# ADR-0001: Use Git as External ERG Log

## Status

Accepted as initial working rule.

## Context

Natural-language chat history makes convergence hard to observe.
Git provides file diffs, commits, branches, and decision records.

## Decision

Use GitHub repository artifacts as external ERG nodes:

- README as stable summary.
- FORMALIZATION as current mathematical model.
- CONVERGENCE as convergence tracker.
- logs as dialogue traces.
- decisions as accepted changes.

## Consequences

The model can be inspected through diffs rather than memory alone.
Unstable ideas must remain outside README until accepted.

""",
    ".gitignore": """__pycache__/
*.pyc
memory_store/
erg_store/generated/
.DS_Store
""",
}


def write_text_if_missing(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return False
    path.write_text(content, encoding="utf-8")
    return True


def scaffold_repo(path_text: str):
    root = resolve_local_path(path_text or "ERG_TAO_math_repo")
    root.mkdir(parents=True, exist_ok=True)
    created = []
    skipped = []
    for rel, content in SCAFFOLD_FILES.items():
        p = root / rel
        if write_text_if_missing(p, content):
            created.append(rel)
        else:
            skipped.append(rel)
    print("scaffold root:", root)
    print("created:", len(created))
    for rel in created:
        print("+", rel)
    if skipped:
        print("skipped existing:", len(skipped))
        for rel in skipped:
            print("=", rel)


def round_log(raw: str, layer_override=None, structure_override=None, limit: int = 8):
    parts = raw.strip().split(maxsplit=2)
    if len(parts) < 3:
        print("usage: python memory_erg_app.py round_log repo_path proposer|critic|synthesizer \"text\"")
        return
    repo_path, role_token, q = parts
    role = ROLE_ALIASES.get(role_token.lower())
    if role is None:
        print("role must be one of:", ", ".join(sorted(ROLE_ALIASES)))
        return
    root = resolve_local_path(repo_path)
    logs = root / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(JST).strftime("%Y%m%d-%H%M%S")
    slug = slugify_for_file(q)
    out = logs / f"{ts}-{role}-{slug}.md"
    content = "# ERG Round Log\n\n"
    content += f"- role: {role}\n"
    content += f"- timestamp: {datetime.now(JST).isoformat(timespec='seconds')}\n"
    content += f"- input: {q}\n\n"
    content += "```text\n"
    content += build_role_packet(role, q, limit=limit, layer_override=layer_override, structure_override=structure_override)
    content += "\n```\n"
    out.write_text(content, encoding="utf-8")
    print("round log written:", out)


# =========================
# CLI
# =========================

USAGE = """usage:
  python memory_erg_app.py add "text" [--layer object|tool|meta] [--structure STRUCTURE]
  python memory_erg_app.py log "text"        # add alias
  python memory_erg_app.py rebuild
  python memory_erg_app.py query "text" [--layer object|tool|meta] [--structure STRUCTURE] [--limit 8]
  python memory_erg_app.py packet "text" [--layer object|tool|meta] [--structure STRUCTURE] [--limit 8]
  python memory_erg_app.py ask "text" [--model model_name] [--layer object|tool|meta] [--structure STRUCTURE] [--limit 8]
  python memory_erg_app.py layer "text"      # classify project/layer/structure
  python memory_erg_app.py route "text"      # math domain router only
  python memory_erg_app.py import seed_logs.jsonl
  python memory_erg_app.py export seed_export.jsonl
  python memory_erg_app.py dedupe
  python memory_erg_app.py prune N           # remove last N nodes
  python memory_erg_app.py role_packet proposer|critic|synthesizer "text" [--layer object|tool|meta] [--structure STRUCTURE] [--limit 8]
  python memory_erg_app.py scaffold_repo path
  python memory_erg_app.py round_log repo_path proposer|critic|synthesizer "text" [--limit 8]
  python memory_erg_app.py status

available STRUCTURE values:
  slot_generator, symmetry_action, graph_relation, algebraic_operation, category_diagram,
  local_global, state_transition, cellular_lattice, order_lattice, logic_constraint,
  coding_information, optimization_flow, rewriting_language, recursion_fixedpoint,
  unknown_structure
"""

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(USAGE)
        sys.exit()

    cmd = sys.argv[1]

    try:
        text, model, layer_override, structure_override, limit = parse_optional_args(sys.argv[2:])
    except ValueError as e:
        print("argument error:", e)
        sys.exit(1)

    if cmd in {"add", "log"}:
        if not text:
            print("text required")
            sys.exit(1)
        add(text, layer_override=layer_override, structure_override=structure_override)

    elif cmd == "rebuild":
        rebuild()

    elif cmd == "query":
        if not text:
            print("query text required")
            sys.exit(1)
        query(text, layer_override=layer_override, structure_override=structure_override, limit=limit)

    elif cmd == "packet":
        if not text:
            print("query text required")
            sys.exit(1)
        packet(text, layer_override=layer_override, structure_override=structure_override, limit=limit)

    elif cmd == "ask":
        if not text:
            print("query text required")
            sys.exit(1)
        ask(text, model=model, layer_override=layer_override, structure_override=structure_override, limit=limit)

    elif cmd == "layer":
        if not text:
            print("text required")
            sys.exit(1)
        show_layer(text)

    elif cmd == "route":
        if not text:
            print("text required")
            sys.exit(1)
        route(text, structure_override=structure_override)

    elif cmd == "import":
        if not text:
            print("import file path required")
            sys.exit(1)
        import_seed(text)

    elif cmd == "export":
        export_seed(text or "seed_export.jsonl")

    elif cmd == "dedupe":
        dedupe()

    elif cmd == "prune":
        if not text:
            print("usage: python memory_erg_app.py prune N")
            sys.exit(1)
        prune_last(text)

    elif cmd == "role_packet":
        if not text:
            print("usage: python memory_erg_app.py role_packet proposer|critic|synthesizer \"text\"")
            sys.exit(1)
        role_packet(text, layer_override=layer_override, structure_override=structure_override, limit=limit)

    elif cmd == "scaffold_repo":
        scaffold_repo(text or "ERG_TAO_math_repo")

    elif cmd == "round_log":
        if not text:
            print("usage: python memory_erg_app.py round_log repo_path proposer|critic|synthesizer \"text\"")
            sys.exit(1)
        round_log(text, layer_override=layer_override, structure_override=structure_override, limit=limit)

    elif cmd == "status":
        status()

    else:
        print("unknown command:", cmd)
        print(USAGE)
