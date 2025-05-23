{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "c1715d05-6023-46af-a2f1-e8fa35bde545",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "Matplotlib is building the font cache; this may take a moment.\n"
     ]
    }
   ],
   "source": [
    "# 02_confounder_dag_pipeline.py\n",
    "\n",
    "import json\n",
    "import os\n",
    "import networkx as nx\n",
    "import matplotlib.pyplot as plt\n",
    "from sqlalchemy import create_engine, MetaData\n",
    "from dotenv import load_dotenv\n",
    "\n",
    "load_dotenv()\n",
    "\n",
    "# Load database credentials\n",
    "engine = create_engine(\n",
    "    f\"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@\"\n",
    "    f\"{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME', 'dag_review_db')}\"\n",
    ")\n",
    "metadata = MetaData()\n",
    "metadata.reflect(bind=engine)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "5bc2fd61-e770-40ee-bd68-ef2e9b68ec61",
   "metadata": {},
   "outputs": [],
   "source": [
    "def infer_confounders(exposures, outcomes):\n",
    "    # Simple domain-inspired heuristic: suggest age, sex, SES, comorbidities\n",
    "    common_confounders = [\"age\", \"sex\", \"socioeconomic_status\", \"baseline_health\"]\n",
    "    inferred = []\n",
    "    for exposure in exposures:\n",
    "        for outcome in outcomes:\n",
    "            for c in common_confounders:\n",
    "                inferred.append((c, exposure))  # confounder → exposure\n",
    "                inferred.append((c, outcome))   # confounder → outcome\n",
    "    return list(set(inferred)), common_confounders"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 95,
   "id": "3e2e8db4-16a7-424d-bab2-834d2c1b20ab",
   "metadata": {},
   "outputs": [],
   "source": [
    "def propose_dag(study_id):\n",
    "    with engine.connect() as conn:\n",
    "        study = conn.execute(metadata.tables['studies'].select().where(\n",
    "            metadata.tables['studies'].c.id == study_id)).fetchone()\n",
    "        if not study:\n",
    "            print(\"Study not found.\")\n",
    "            return\n",
    "\n",
    "        exposures = [row._mapping['exposure'] for row in conn.execute(\n",
    "            metadata.tables['exposures'].select().where(\n",
    "                metadata.tables['exposures'].c.study_id == study_id))]\n",
    "\n",
    "        outcomes_data = conn.execute(\n",
    "            metadata.tables['outcomes'].select().where(\n",
    "                metadata.tables['outcomes'].c.study_id == study_id)).fetchall()\n",
    "        outcomes = []\n",
    "        for o in outcomes_data:\n",
    "            data = o._mapping.get('data')\n",
    "            if isinstance(data, list) and data and isinstance(data[0], dict) and 'value' in data[0]:\n",
    "                outcomes.append(data[0]['value'])\n",
    "            else:\n",
    "                outcomes.append(str(data))\n",
    "\n",
    "        if exposures:\n",
    "            inferred_edges, confounders = infer_confounders(exposures, outcomes)\n",
    "            graph_inputs = exposures + confounders\n",
    "            print(\"Building DAG using exposures and inferred confounders.\")\n",
    "        else:\n",
    "            print(\"No exposures found — switching to eligibility criteria and baseline characteristics.\")\n",
    "            inferred_edges = []\n",
    "            confounders = []\n",
    "            eligibility_data = conn.execute(\n",
    "                metadata.tables['eligibility_criteria'].select().where(\n",
    "                    metadata.tables['eligibility_criteria'].c.study_id == study_id)).fetchall()\n",
    "            for row in eligibility_data:\n",
    "                confounders.append(row._mapping['criteria'])\n",
    "            graph_inputs = confounders\n",
    "\n",
    "        dag = nx.DiGraph()\n",
    "        dag.add_nodes_from(set(graph_inputs + outcomes))\n",
    "        dag.add_edges_from([(c, o) for c in graph_inputs for o in outcomes if c and o])\n",
    "        dag.add_edges_from([edge for edge in inferred_edges if edge[0] and edge[1]])\n",
    "\n",
    "        def shorten(label, max_len=40):\n",
    "            return label if len(label) <= max_len else label[:max_len] + \"...\"\n",
    "\n",
    "        for node in dag.nodes:\n",
    "            dag.nodes[node]['type'] = 'confounder' if node in confounders else ('exposure' if node in exposures else 'outcome')\n",
    "            dag.nodes[node]['label'] = shorten(node)\n",
    "\n",
    "        # Clear existing DAG for the study\n",
    "        with engine.begin() as trans_conn:\n",
    "            # First delete edges to avoid FK violation\n",
    "            trans_conn.execute(metadata.tables['dag_edges'].delete().where(\n",
    "                metadata.tables['dag_edges'].c.study_id == study_id))\n",
    "            trans_conn.execute(metadata.tables['dag_nodes'].delete().where(\n",
    "                metadata.tables['dag_nodes'].c.study_id == study_id))\n",
    "\n",
    "            for node in dag.nodes:\n",
    "                trans_conn.execute(metadata.tables['dag_nodes'].insert().values(\n",
    "                    study_id=study_id,\n",
    "                    node_label=node,\n",
    "                    node_type=dag.nodes[node]['type'],\n",
    "                    source='llm'\n",
    "                ))\n",
    "\n",
    "            for edge in dag.edges:\n",
    "                from_label, to_label = edge\n",
    "                from_node_id = trans_conn.execute(\n",
    "                    metadata.tables['dag_nodes'].select().where(\n",
    "                        metadata.tables['dag_nodes'].c.study_id == study_id,\n",
    "                        metadata.tables['dag_nodes'].c.node_label == from_label\n",
    "                    )).scalar()\n",
    "                to_node_id = trans_conn.execute(\n",
    "                    metadata.tables['dag_nodes'].select().where(\n",
    "                        metadata.tables['dag_nodes'].c.study_id == study_id,\n",
    "                        metadata.tables['dag_nodes'].c.node_label == to_label\n",
    "                    )).scalar()\n",
    "\n",
    "                if from_node_id and to_node_id:\n",
    "                    trans_conn.execute(metadata.tables['dag_edges'].insert().values(\n",
    "                        study_id=study_id,\n",
    "                        from_node_id=from_node_id,\n",
    "                        to_node_id=to_node_id,\n",
    "                        relation_type='llm',\n",
    "                        confidence=1.0\n",
    "                    ))\n",
    "\n",
    "        # Export DAGitty text format\n",
    "        dagitty = \"dag {\"\n",
    "        for node in dag.nodes:\n",
    "            safe_node = node.replace('\"', \"'\")\n",
    "            dagitty += f\"\\n\\\"{safe_node}\\\"\"\n",
    "        for src, tgt in dag.edges:\n",
    "            dagitty += f\"\\n\\\"{src}\\\" -> \\\"{tgt}\\\"\"\n",
    "        dagitty += \"\\n}\"\n",
    "\n",
    "        dagitty_txt_path = f\"dagitty_study_{study_id}.txt\"\n",
    "        with open(dagitty_txt_path, \"w\") as f:\n",
    "            f.write(dagitty)\n",
    "\n",
    "        # Create R Markdown file to render DAG\n",
    "        rmd_path = f\"dagitty_study_{study_id}.Rmd\"\n",
    "        rmd_content = f\"\"\"\n",
    "---\n",
    "title: \"DAGitty DAG for Study {study_id}\"\n",
    "output: html_document\n",
    "---\n",
    "\n",
    "```{{r setup, include=FALSE}}\n",
    "library(dagitty)\n",
    "library(ggdag)\n",
    "```\n",
    "\n",
    "```{{r load-and-plot-dag}}\n",
    "dag_text <- readLines(\"dagitty_study_2.txt\")\n",
    "dag <- dagitty(paste(dag_text, collapse = \"\\n\"))\n",
    "\n",
    "ggdag(dag, text = FALSE, use_labels = \"none\") +\n",
    "  geom_dag_edges() +\n",
    "  geom_dag_text_repel(aes(label = name), size = 3, segment.size = 0.2, box.padding = 0.3, point.padding = 0.25) +\n",
    "  theme_dag()\n",
    "```\n",
    "\"\"\"\n",
    "        with open(dagitty_txt_path, \"w\") as f:\n",
    "            f.write(dagitty + \"\\n\")\n",
    "\n",
    "        import subprocess\n",
    "        subprocess.run([\"Rscript\", \"-e\", f\"rmarkdown::render('{rmd_path}')\"])\n",
    "        html_path = f\"dagitty_study_{study_id}.html\"\n",
    "        if os.path.exists(html_path):\n",
    "            import webbrowser\n",
    "            webbrowser.open(f\"file://{os.path.abspath(html_path)}\")\n",
    "    return {\n",
    "        \"graph\": dag,\n",
    "        \"dagitty\": dagitty,\n",
    "        \"nodes\": list(dag.nodes),\n",
    "        \"edges\": list(dag.edges),\n",
    "        \"dagviz\": None  # placeholder if needed later\n",
    "    }"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 96,
   "id": "73f98ae2-66d7-46e2-89f7-4b4ccce2093e",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "No exposures found — switching to eligibility criteria and baseline characteristics.\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "\n",
      "\n",
      "processing file: dagitty_study_2.Rmd\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "1/4                    \n",
      "2/4 [setup]            \n",
      "3/4                    \n",
      "4/4 [load-and-plot-dag]\n",
      "/opt/homebrew/bin/pandoc +RTS -K512m -RTS dagitty_study_2.knit.md --to html4 --from markdown+autolink_bare_uris+tex_math_single_backslash --output dagitty_study_2.html --lua-filter /Library/Frameworks/R.framework/Versions/4.5-arm64/Resources/library/rmarkdown/rmarkdown/lua/pagebreak.lua --lua-filter /Library/Frameworks/R.framework/Versions/4.5-arm64/Resources/library/rmarkdown/rmarkdown/lua/latex-div.lua --lua-filter /Library/Frameworks/R.framework/Versions/4.5-arm64/Resources/library/rmarkdown/rmarkdown/lua/table-classes.lua --embed-resources --standalone --variable bs3=TRUE --section-divs --template /Library/Frameworks/R.framework/Versions/4.5-arm64/Resources/library/rmarkdown/rmd/h/default.html --no-highlight --variable highlightjs=1 --variable theme=bootstrap --mathjax --variable 'mathjax-url=https://mathjax.rstudio.com/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML' --include-in-header /var/folders/g5/fk0fxc8n0b56nqrtwj8ywdlm0000gn/T//Rtmp2M4FBl/rmarkdown-str14f5a2b0c7561.html \n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "output file: dagitty_study_2.knit.md\n",
      "\n",
      "\n",
      "Output created: dagitty_study_2.html\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "{'graph': <networkx.classes.digraph.DiGraph at 0x11f6d77c0>,\n",
       " 'dagitty': 'dag {\\n\"Echocardiographic parameters such as left ventricular ejection fraction, left ventricular mass index (LVMI), left ventricular hypertrophy, left atrial enlargement and diastolic function\"\\n\"Patients with type 2 diabetes mellitus (T2DM) with no history of cardiovascular disease (CVD)\"\\n\"Patients with type 2 diabetes mellitus (T2DM) with no history of cardiovascular disease (CVD)\" -> \"Echocardiographic parameters such as left ventricular ejection fraction, left ventricular mass index (LVMI), left ventricular hypertrophy, left atrial enlargement and diastolic function\"\\n}',\n",
       " 'nodes': ['Echocardiographic parameters such as left ventricular ejection fraction, left ventricular mass index (LVMI), left ventricular hypertrophy, left atrial enlargement and diastolic function',\n",
       "  'Patients with type 2 diabetes mellitus (T2DM) with no history of cardiovascular disease (CVD)'],\n",
       " 'edges': [('Patients with type 2 diabetes mellitus (T2DM) with no history of cardiovascular disease (CVD)',\n",
       "   'Echocardiographic parameters such as left ventricular ejection fraction, left ventricular mass index (LVMI), left ventricular hypertrophy, left atrial enlargement and diastolic function')],\n",
       " 'dagviz': None}"
      ]
     },
     "execution_count": 96,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "propose_dag(2)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.16"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
