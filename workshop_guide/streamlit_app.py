from pathlib import Path

import streamlit as st

from components import is_session_complete

_DIR = Path(__file__).parent


def _title(session_num: int, label: str) -> str:
    check = " :green[:material/check_circle:]" if is_session_complete(session_num) else ""
    return f"{session_num}. {label}{check}"


st.set_page_config(
    page_title="HIIVE Data Intelligence Workshop",
    page_icon=":material/trending_up:",
    layout="wide",
)

st.logo(
    str(_DIR / "static" / "snowflake_full_logo.png"),
    icon_image=str(_DIR / "static" / "snowflake_logo.png"),
)

page = st.navigation(
    {
        "": [
            st.Page("app_pages/home.py", title="Home", icon=":material/home:"),
            st.Page("app_pages/getting_started.py", title="Getting Started", icon=":material/rocket_launch:"),
            st.Page("app_pages/agenda.py", title="Agenda", icon=":material/calendar_today:"),
        ],
        "Block 1: Data & Intelligence": [
            st.Page("app_pages/session_01.py", title=_title(1, "Data Prep"), icon=":material/database:"),
            st.Page("app_pages/session_02.py", title=_title(2, "Cortex Analyst & Semantic Views"), icon=":material/chat:"),
            st.Page("app_pages/session_03.py", title=_title(3, "Cortex Search"), icon=":material/search:"),
        ],
        "Block 2: Agents & Apps": [
            st.Page("app_pages/session_04.py", title=_title(4, "Cortex Agents"), icon=":material/smart_toy:"),
            st.Page("app_pages/session_05.py", title=_title(5, "CoWork"), icon=":material/group:"),
            st.Page("app_pages/session_06.py", title=_title(6, "Streamlit"), icon=":material/web:"),
        ],
        "Block 3: Monitoring & Quality": [
            st.Page("app_pages/session_07.py", title=_title(7, "DMF & Monitoring"), icon=":material/monitoring:"),
        ],
        "Block 4: Data Pipelines": [
            st.Page("app_pages/session_08.py", title=_title(8, "dbt Projects"), icon=":material/transform:"),
            st.Page("app_pages/session_09.py", title=_title(9, "dbt Projects (Hands-On)"), icon=":material/terminal:"),
        ],
        "Reference": [
            st.Page("app_pages/reference_coco.py", title="Cortex Code Plugin", icon=":material/extension:"),
        ],
    },
    position="sidebar",
)

page.run()
