import itertools
from collections import deque

import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Bipartite Graphs for Job Assignment", page_icon="🔗", layout="wide")

# ---------- Helper ----------
def draw_bipartite(left, right, edges, highlight=None, left_title="", right_title=""):
    """Gambar graf bipartit: kiri = left, kanan = right. highlight = set edge yang diberi warna merah."""
    highlight = highlight or set()
    fig, ax = plt.subplots(figsize=(5, 3.5))
    pos = {}
    for i, v in enumerate(left):
        pos[v] = (0, -i)
    for i, v in enumerate(right):
        pos[v] = (1, -i)
    for u, v in edges:
        x = [pos[u][0], pos[v][0]]
        y = [pos[u][1], pos[v][1]]
        hl = (u, v) in highlight
        ax.plot(x, y, color="crimson" if hl else "#3b6aa8", lw=3 if hl else 1.5, zorder=1)
    for v, (x, y) in pos.items():
        ax.scatter([x], [y], s=1400, color="#76c7c0", edgecolor="#a3237a", linewidth=2, zorder=2)
        ax.text(x, y, v, ha="center", va="center", fontsize=10, zorder=3)
    ax.text(0, 0.7, left_title, ha="center", fontsize=11, weight="bold")
    ax.text(1, 0.7, right_title, ha="center", fontsize=11, weight="bold")
    ax.set_xlim(-0.3, 1.3)
    ax.set_ylim(-max(len(left), len(right)) + 0.4, 1.1)
    ax.axis("off")
    return fig


def is_bipartite(vertices, edges):
    """Cek bipartit dengan pewarnaan 2 warna (BFS)."""
    adj = {v: [] for v in vertices}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    color = {}
    for s in vertices:
        if s in color:
            continue
        color[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for w in adj[u]:
                if w == u:
                    return False, {}
                if w not in color:
                    color[w] = 1 - color[u]
                    q.append(w)
                elif color[w] == color[u]:
                    return False, {}
    return True, color


# ---------- Sidebar ----------
st.sidebar.title("Group 3 – Discrete Math")
st.sidebar.caption("Bipartite Graphs for Job Assignment")
page = st.sidebar.radio(
    "Menu",
    [
        "Home",
        "1. Introduction to the Graph",
        "2. Types of Graphs",
        "3. Bipartite Graph",
        "4. Complete Bipartite Graph",
        "5. Job Assignment",
        "6. Conclusion",
    ],
)
st.sidebar.markdown("---")
st.sidebar.markdown(
    "**Presented by:**  \n"
    "Muhammad Dzaky Herwandi (021202600035)  \n"
    "Ucok Aulian Sihombing (021202600021)  \n"
    "Wianda Nandita Zebua (021202600006)"
)

# ---------- Pages ----------
if page == "Home":
    st.title("Bipartite Graphs for Job Assignment")
    st.subheader("Discrete Math – Group 3")
    st.write("Presented by:")
    st.markdown(
        "- Muhammad Dzaky Herwandi (021202600035)\n"
        "- Ucok Aulian Sihombing (021202600021)\n"
        "- Wianda Nandita Zebua (021202600006)"
    )
    st.markdown("### Table of Contents")
    st.markdown(
        "1. Introduction to the Graph\n"
        "2. Types of Graphs\n"
        "3. Bipartite Graph\n"
        "4. Complete Bipartite Graph\n"
        "5. Job Assignment\n"
        "6. Conclusion"
    )
    st.info("Pilih materi lewat menu di sebelah kiri.")

elif page == "1. Introduction to the Graph":
    st.header("Introduction to the Graph")
    st.markdown(
        "- A graph is written as **G = (V, E)**, where **V** is a set of vertices (nodes) "
        "and **E** is a set of edges connecting them.\n"
        "- **Undirected graph:** the edges have no direction.\n"
        "- **Directed graph (digraph):** the edges have a direction."
    )
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**(a) Undirected graph**")
        fig, ax = plt.subplots(figsize=(4, 3))
        pts = {"1": (0, 1), "2": (1, 1.2), "3": (0.5, 0.5), "4": (-0.2, 0), "5": (1.1, 0)}
        for u, v in [("1", "2"), ("1", "3"), ("2", "3"), ("3", "4"), ("3", "5"), ("4", "5")]:
            ax.plot([pts[u][0], pts[v][0]], [pts[u][1], pts[v][1]], color="#3b6aa8")
        for k, (x, y) in pts.items():
            ax.scatter([x], [y], s=500, color="white", edgecolor="#3b6aa8", zorder=2)
            ax.text(x, y, k, ha="center", va="center")
        ax.axis("off")
        st.pyplot(fig)
    with c2:
        st.markdown("**(b) Directed graph**")
        fig, ax = plt.subplots(figsize=(4, 3))
        for u, v in [("1", "2"), ("1", "3"), ("3", "2"), ("3", "4"), ("5", "3"), ("4", "5")]:
            ax.annotate("", xy=pts[v], xytext=pts[u],
                        arrowprops=dict(arrowstyle="->", color="#3b6aa8", shrinkA=14, shrinkB=14))
        for k, (x, y) in pts.items():
            ax.scatter([x], [y], s=500, color="white", edgecolor="#3b6aa8", zorder=2)
            ax.text(x, y, k, ha="center", va="center")
        ax.axis("off")
        st.pyplot(fig)

elif page == "2. Types of Graphs":
    st.header("Types of Graphs")
    c1, c2, c3 = st.columns(3)
    c1.markdown("#### Simple Graph")
    c1.write("There are no loops (no edge from a vertex to itself) and no multiple edges "
             "(no duplicate connections).")
    c2.markdown("#### Multigraph")
    c2.write("Two vertices can be connected by more than one edge.")
    c3.markdown("#### Pseudograph")
    c3.write("Contains loops and multiple edges.")

elif page == "3. Bipartite Graph":
    st.header("Bipartite Graph")
    st.write(
        "A graph G = (V, E) is said to be bipartite if the vertex set V can be divided into two "
        "disjoint subsets V1 and V2 such that every edge in E connects a vertex in V1 to a vertex "
        "in V2. No edge in the graph connects two vertices within V1 or two vertices within V2."
    )
    edges = [("A", "X"), ("A", "Y"), ("B", "X"), ("B", "Y"), ("C", "Y")]
    st.pyplot(draw_bipartite(["A", "B", "C"], ["X", "Y", "Z"], edges, left_title="V1", right_title="V2"))
    st.caption("Contoh: V1 = {A, B, C}, V2 = {X, Y, Z}. Z tidak punya edge, tetapi graf tetap bipartit.")

    st.markdown("#### Coba sendiri: cek apakah suatu graf bipartit")
    txt = st.text_input("Masukkan edge (pisahkan dengan koma, contoh: A-B, B-C, C-A)", "A-X, A-Y, B-X, B-Y, C-Y")
    try:
        es = [tuple(p.strip().split("-")) for p in txt.split(",") if p.strip()]
        vs = sorted({v for e in es for v in e})
        ok, col = is_bipartite(vs, es)
        if ok:
            st.success("Graf ini BIPARTIT.")
            st.write("V1 =", [v for v in vs if col[v] == 0], "| V2 =", [v for v in vs if col[v] == 1])
        else:
            st.error("Graf ini BUKAN bipartit (ada siklus ganjil atau loop).")
    except Exception:
        st.warning("Format salah. Gunakan format A-B, B-C.")

elif page == "4. Complete Bipartite Graph":
    st.header("Complete Bipartite Graph")
    st.write(
        "A complete bipartite graph or **biclique** is a special type of bipartite graph in which "
        "every vertex in the first set is connected to every vertex in the second set."
    )
    m = st.slider("Jumlah vertex di himpunan pertama (m)", 1, 5, 4)
    n = st.slider("Jumlah vertex di himpunan kedua (n)", 1, 5, 3)
    left = [chr(65 + i) for i in range(m)]
    right = [chr(80 + i) for i in range(n)]
    edges = [(u, v) for u in left for v in right]
    st.pyplot(draw_bipartite(left, right, edges))
    st.success(f"K({m},{n}) memiliki {m} × {n} = {m * n} edge.")

elif page == "5. Job Assignment":
    st.header("Job Assignment")
    st.markdown(
        "- Three jobs are to be distributed among 3 persons (A, B, C).\n"
        "- Each job can only be done by persons who are qualified for it.\n"
        "- The table is drawn as a bipartite graph: jobs on the left, persons on the right, "
        "and an edge means \"qualified\"."
    )
    jobs = ["Admin", "Programmer", "Professor"]
    persons = ["A", "B", "C"]
    default = {"Admin": ["A", "C"], "Programmer": ["B", "C"], "Professor": ["A", "B"]}

    tab1, tab2 = st.tabs(["Kasus awal (tabel qualified)", "Complete Bipartite Case K(3,3)"])

    with tab1:
        st.markdown("Centang kolom untuk mengubah siapa yang qualified:")
        cols = st.columns(4)
        cols[0].markdown("**Job**")
        for i, p in enumerate(persons):
            cols[i + 1].markdown(f"**{p}**")
        edges = []
        for j in jobs:
            cols = st.columns(4)
            cols[0].write(j)
            for i, p in enumerate(persons):
                if cols[i + 1].checkbox("qualified", value=p in default[j], key=f"q_{j}_{p}",
                                        label_visibility="collapsed"):
                    edges.append((j, p))
        sols = [perm for perm in itertools.permutations(persons)
                if all((j, p) in edges for j, p in zip(jobs, perm))]
        c1, c2 = st.columns(2)
        with c1:
            hl = set(zip(jobs, sols[0])) if sols else set()
            st.pyplot(draw_bipartite(jobs, persons, edges, highlight=hl, left_title="Jobs", right_title="Persons"))
        with c2:
            if sols:
                st.success(f"Ada {len(sols)} cara pembagian kerja yang valid.")
                for s in sols:
                    st.write(" | ".join(f"{j} → {p}" for j, p in zip(jobs, s)))
                st.caption("Edge merah = salah satu contoh assignment (perfect matching).")
            else:
                st.error("Tidak ada pembagian kerja yang memungkinkan semua job terisi.")

    with tab2:
        st.write("Case: every person must work part-time in every department. "
                 "Every job is connected to every person.")
        edges = [(j, p) for j in jobs for p in persons]
        st.pyplot(draw_bipartite(jobs, persons, edges, left_title="Jobs", right_title="Persons"))
        st.success("The graph becomes a complete bipartite graph K(3,3) with 3 × 3 = 9 edges.")

elif page == "6. Conclusion":
    st.header("Conclusion")
    st.write(
        "In job assignment problems, bipartite graphs help represent the relationship between two "
        "distinct sets — workers and jobs — where edges show possible assignments. When every worker "
        "is connected to every job, the graph becomes a complete bipartite graph, showing full "
        "connectivity. This concept allows tasks to be distributed efficiently and visually "
        "demonstrates how assignments can be optimized."
    )
    st.balloons()
    st.markdown("**Thank you!**")
