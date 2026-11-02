
import streamlit as st
import pandas as pd
import altair as alt
from pathlib import Path

# ---------------------------------------------------------
# CONFIGURAÇÃO
# ---------------------------------------------------------

st.set_page_config(
    page_title="FinCred | Painel Executivo",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# ESTILO
# ---------------------------------------------------------

st.markdown("""
<style>
    :root {
        --paper: #F8F5F3;
        --surface: #FFFFFF;
        --ink: #2C2228;
        --muted: #5E5259;
        --plum: #482638;
        --berry: #70445B;
        --mauve: #89556F;
        --rose: #B4879A;
        --line: #DED2D8;
    }

    .stApp,
    [data-testid="stAppViewContainer"] {
        background: var(--paper);
        color: var(--ink);
    }

    .block-container {
        max-width: 1500px;
        padding-top: 3rem;
        padding-bottom: 3.5rem;
    }

    h1, h2, h3 {
        color: var(--ink);
        font-family: "Segoe UI", Arial, sans-serif;
        letter-spacing: -0.035em;
    }

    h1 {
        font-size: clamp(2.6rem, 4vw, 3.8rem) !important;
        line-height: 1.05 !important;
        margin-bottom: 0.3rem !important;
    }

    h2, h3 {
        letter-spacing: -0.02em;
    }

    [data-testid="stCaptionContainer"] {
        color: var(--muted);
    }

    [data-testid="stMetric"] {
        background: var(--surface);
        border: 1px solid var(--line);
        border-top: 3px solid var(--mauve);
        padding: 1.1rem 1.2rem;
        border-radius: 4px;
        box-shadow: 0 5px 18px rgba(48, 37, 44, 0.035);
        min-height: 112px;
    }

    [data-testid="stMetricLabel"] {
        color: var(--muted);
        font-size: 0.76rem;
        font-weight: 650;
        letter-spacing: 0.075em;
        text-transform: uppercase;
    }

    [data-testid="stMetricValue"] {
        color: var(--plum);
        font-family: "Segoe UI", Arial, sans-serif;
        font-weight: 700;
    }

    section[data-testid="stSidebar"] {
        background: #F0E8EC;
        border-right: 1px solid var(--line);
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: var(--plum);
    }

    div[data-testid="stDataFrame"] {
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 4px;
    }

    hr {
        border-color: var(--line);
    }

    div[data-testid="stToolbar"] {
        background: transparent;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# FUNÇÕES
# ---------------------------------------------------------

def format_brl(value):
    return (
        f"R$ {value:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "streamlit"


@st.cache_data
def load_data():
    portfolio = pd.read_csv(DATA_DIR / "vw_credit_portfolio.csv")
    installments = pd.read_csv(DATA_DIR / "vw_installments_current.csv")

    portfolio["contract_date"] = pd.to_datetime(
        portfolio["contract_date"], errors="coerce"
    )
    portfolio["ano_contratacao"] = portfolio["contract_date"].dt.year
    installments["due_date"] = pd.to_datetime(
        installments["due_date"], errors="coerce"
    )
    installments["payment_date"] = pd.to_datetime(
        installments["payment_date"], errors="coerce"
    )

    return portfolio, installments


# ---------------------------------------------------------
# CABEÇALHO
# ---------------------------------------------------------

st.title("FinCred")
st.caption("PAINEL EXECUTIVO  |  CARTEIRA DE CRÉDITO")
st.divider()


# ---------------------------------------------------------
# CARREGAMENTO
# ---------------------------------------------------------

try:
    portfolio, installments = load_data()

    if portfolio.empty:
        st.warning("Não há contratos disponíveis para análise.")
        st.stop()

    # -----------------------------------------------------
    # FILTROS
    # -----------------------------------------------------

    st.sidebar.title("Filtros")
    st.sidebar.caption("Personalize a visualização da carteira.")

    years = sorted(
        portfolio["ano_contratacao"].dropna().unique().tolist()
    )

    selected_years = st.sidebar.multiselect(
        "Ano de contratação",
        options=years,
        default=[],
        format_func=lambda x: str(int(x)),
    )

    situations = ["EM_DIA", "EM_ATRASO", "INADIMPLENTE"]

    selected_situations = st.sidebar.multiselect(
        "Situação do contrato",
        options=situations,
        default=[],
    )

    st.sidebar.divider()
    st.sidebar.caption("Cópia estática dos dados de demonstração.")
    st.sidebar.caption("Referência dos indicadores: 31/12/2026")

    # -----------------------------------------------------
    # APLICAÇÃO DOS FILTROS
    # -----------------------------------------------------

    filtered = portfolio.copy()

    if selected_years:
        filtered = filtered[
            filtered["ano_contratacao"].isin(selected_years)
        ]

    if selected_situations:
        filtered = filtered[
            filtered["contract_situation"].isin(selected_situations)
        ]

    selected_contract_ids = filtered["contract_id"].unique()

    filtered_installments = installments[
        installments["contract_id"].isin(selected_contract_ids)
    ].copy()

    if filtered.empty:
        st.warning("Nenhum contrato encontrado para os filtros selecionados.")
        st.stop()

    # -----------------------------------------------------
    # INDICADORES EXECUTIVOS
    # -----------------------------------------------------

    total_contracts = filtered["contract_id"].nunique()

    total_portfolio = filtered["total_installment_amount"].sum()

    open_balance = filtered["open_installment_amount"].sum()

    total_paid = filtered["total_paid_amount"].sum()

    contrato_quitado = (filtered["qt_installment_total"] == filtered["qt_installment_paid"]).sum()

    delinquent_contracts = (
        filtered["contract_situation"] == "INADIMPLENTE"
    ).sum()

    delinquency_rate = (
        delinquent_contracts / total_contracts * 100
        if total_contracts > 0 else 0
    )

    st.subheader("Visão geral da carteira")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Contratos",
        total_contracts,
    )

    col2.metric(
        "Contratos quitados",
        contrato_quitado,
    )

    col3.metric(
        "Contratos inadimplentes",
        delinquent_contracts,
    )

    col4.metric(
        "Taxa de inadimplência",
        f"{delinquency_rate:.1f}%".replace(".", ","),
    )



    # -----------------------------------------------------
    # SEGUNDA LINHA DE INDICADORES
    # -----------------------------------------------------

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Valor total das parcelas",
        f"R$ {total_portfolio / 1_000_000:.1f} milhões".replace(".", ","),
        help=format_brl(total_portfolio),
    )

    col2.metric(
        "Saldo em aberto",
        f"R$ {open_balance / 1_000_000:.1f} milhões".replace(".", ","),
        help=format_brl(open_balance),
    )

    col3.metric(
        "Valor total pago",
        f"R$ {total_paid / 1_000_000:.1f} milhões".replace(".", ","),
        help=format_brl(total_paid),
    )

    st.divider()

    # -----------------------------------------------------
    # ANÁLISE DA CARTEIRA
    # -----------------------------------------------------

    st.subheader("Análise da carteira")

    left, right = st.columns(2)

    with left:
        st.markdown("**Contratos por situação**")

        situation_order = [
            "EM_DIA",
            "EM_ATRASO",
            "INADIMPLENTE",
        ]

        situation_df = (
            filtered["contract_situation"]
            .value_counts()
            .reindex(situation_order, fill_value=0)
            .rename_axis("Situação")
            .reset_index(name="Contratos")
        )

        situation_chart = alt.Chart(situation_df).mark_bar(
            cornerRadiusEnd=5
        ).encode(
            x=alt.X(
                "Situação:N",
                sort=situation_order,
                axis=alt.Axis(title=None, labelAngle=0),
            ),
            y=alt.Y(
                "Contratos:Q",
                axis=alt.Axis(title="Quantidade de contratos"),
            ),
            color=alt.Color(
                "Situação:N",
                scale=alt.Scale(
                    domain=situation_order,
                    range=["#8F5D75", "#B4879A", "#482638"],
                ),
                legend=None,
            ),
            tooltip=["Situação", "Contratos"],
        ).properties(height=300).configure(background="transparent").configure_view(stroke=None).configure_axis(labelColor="#51454C", titleColor="#51454C", gridColor="#E7DFE3", domainColor="#C9BBC2", tickColor="#C9BBC2", labelFont="Arial", titleFont="Arial")

        st.altair_chart(situation_chart, use_container_width=True)

    with right:
        st.markdown("**Parcelas por status**")

        status_order = ["PAGA", "PENDENTE", "ATRASADA"]

        status_df = (
            filtered_installments["installment_status"]
            .value_counts()
            .reindex(status_order, fill_value=0)
            .rename_axis("Status")
            .reset_index(name="Parcelas")
        )

        status_chart = alt.Chart(status_df).mark_bar(
            cornerRadiusEnd=5
        ).encode(
            x=alt.X(
                "Status:N",
                sort=status_order,
                axis=alt.Axis(title=None, labelAngle=0),
            ),
            y=alt.Y(
                "Parcelas:Q",
                axis=alt.Axis(title="Quantidade de parcelas"),
            ),
            color=alt.Color(
                "Status:N",
                scale=alt.Scale(
                    domain=status_order,
                    range=["#8F5D75", "#746970", "#B4879A"],
                ),
                legend=None,
            ),
            tooltip=["Status", "Parcelas"],
        ).properties(height=300).configure(background="transparent").configure_view(stroke=None).configure_axis(labelColor="#51454C", titleColor="#51454C", gridColor="#E7DFE3", domainColor="#C9BBC2", tickColor="#C9BBC2", labelFont="Arial", titleFont="Arial")

        st.altair_chart(status_chart, use_container_width=True)

    st.divider()

    # -----------------------------------------------------
    # ORIGINAÇÃO ANUAL
    # -----------------------------------------------------

    st.subheader("Originação de crédito")

    annual_df = (
        filtered.groupby("ano_contratacao")
        .agg(
            contratos=("contract_id", "nunique"),
            valor_carteira=("total_installment_amount", "sum"),
        )
        .reset_index()
    )

    annual_df["ano_contratacao"] = (
        annual_df["ano_contratacao"].astype(str)
    )

    annual_chart = alt.Chart(annual_df).mark_bar(
        cornerRadiusEnd=5,
        color="#70445B",
    ).encode(
        x=alt.X(
            "ano_contratacao:N",
            axis=alt.Axis(title=None),
        ),
        y=alt.Y(
            "contratos:Q",
            axis=alt.Axis(title="Quantidade de contratos"),
        ),
        tooltip=[
            alt.Tooltip("ano_contratacao:N", title="Ano"),
            alt.Tooltip("contratos:Q", title="Contratos"),
            alt.Tooltip(
                "valor_carteira:Q",
                title="Valor da carteira",
                format=",.2f",
            ),
        ],
    ).properties(height=300).configure(background="transparent").configure_view(stroke=None).configure_axis(labelColor="#51454C", titleColor="#51454C", gridColor="#E7DFE3", domainColor="#C9BBC2", tickColor="#C9BBC2", labelFont="Arial", titleFont="Arial")

    st.altair_chart(annual_chart, use_container_width=True)

    st.divider()

    # -----------------------------------------------------
    # FAIXAS DE ATRASO
    # -----------------------------------------------------

    st.subheader("Análise de atraso")

    overdue = filtered_installments[
        filtered_installments["installment_status"] == "ATRASADA"
    ].copy()

    if not overdue.empty:
        overdue["faixa_atraso"] = pd.cut(
            overdue["days_late"],
            bins=[0, 30, 60, 90, 180, 365, float("inf")],
            labels=[
                "1 a 30 dias",
                "31 a 60 dias",
                "61 a 90 dias",
                "91 a 180 dias",
                "181 a 365 dias",
                "Mais de 365 dias",
            ],
            include_lowest=False,
        )

        aging_df = (
            overdue.groupby(
                "faixa_atraso",
                observed=False,
            )
            .size()
            .reset_index(name="Parcelas")
        )

        aging_chart = alt.Chart(aging_df).mark_bar(
            cornerRadiusEnd=5,
            color="#482638",
        ).encode(
            x=alt.X(
                "faixa_atraso:N",
                sort=[
                    "1 a 30 dias",
                    "31 a 60 dias",
                    "61 a 90 dias",
                    "91 a 180 dias",
                    "181 a 365 dias",
                    "Mais de 365 dias",
                ],
                axis=alt.Axis(title=None, labelAngle=-25),
            ),
            y=alt.Y(
                "Parcelas:Q",
                axis=alt.Axis(title="Quantidade de parcelas"),
            ),
            tooltip=["faixa_atraso", "Parcelas"],
        ).properties(height=300).configure(background="transparent").configure_view(stroke=None).configure_axis(labelColor="#51454C", titleColor="#51454C", gridColor="#E7DFE3", domainColor="#C9BBC2", tickColor="#C9BBC2", labelFont="Arial", titleFont="Arial")

        st.altair_chart(aging_chart, use_container_width=True)

    else:
        st.info("Não há parcelas atrasadas para os filtros selecionados.")

    st.divider()

    # -----------------------------------------------------
    # JUROS RECEBIDOS
    # -----------------------------------------------------

    st.subheader("Juros recebidos")

    interest_paid = filtered_installments[
        (filtered_installments["installment_status"] == "PAGA")
        & filtered_installments["interest_amount"].notna()
        & filtered_installments["payment_date"].notna()
    ].copy()
    interest_paid["payment_date"] = pd.to_datetime(
        interest_paid["payment_date"], errors="coerce"
    )
    interest_paid = interest_paid.dropna(subset=["payment_date"])

    if not interest_paid.empty:
        total_interest_received = interest_paid["interest_amount"].sum()
        total_contracted_amount = filtered["contracted_amount"].sum()
        realized_interest_pct = (
            total_interest_received / total_contracted_amount * 100
            if total_contracted_amount > 0 else 0
        )

        interest_metric, yield_metric = st.columns(2)
        interest_metric.metric(
            "Juros recebidos",
            format_brl(total_interest_received),
        )
        yield_metric.metric(
            "Juros recebidos sobre valor contratado",
            f"{realized_interest_pct:.2f}%".replace(".", ","),
            help="Juros efetivamente registrados nos pagamentos divididos pelo valor original contratado.",
        )

        st.caption(
            "Valores realizados, sem multas. O percentual é acumulado até a data "
            "e não representa uma taxa anualizada."
        )

        monthly_interest = (
            interest_paid.assign(
                mes=interest_paid["payment_date"].dt.to_period("M").dt.to_timestamp()
            )
            .groupby("mes", as_index=False)
            .agg(juros_recebidos=("interest_amount", "sum"))
            .sort_values("mes")
        )
        monthly_interest["juros_acumulados"] = (
            monthly_interest["juros_recebidos"].cumsum()
        )

        cohort_interest = (
            interest_paid.groupby("contract_id", as_index=False)
            .agg(juros_recebidos=("interest_amount", "sum"))
        )
        cohort_df = (
            filtered[["contract_id", "ano_contratacao", "contracted_amount"]]
            .drop_duplicates("contract_id")
            .merge(cohort_interest, on="contract_id", how="left")
        )
        cohort_df["juros_recebidos"] = cohort_df["juros_recebidos"].fillna(0)
        cohort_df = (
            cohort_df.groupby("ano_contratacao", as_index=False)
            .agg(
                juros_recebidos=("juros_recebidos", "sum"),
                valor_contratado=("contracted_amount", "sum"),
            )
            .sort_values("ano_contratacao")
        )
        cohort_df["juros_sobre_contratado_pct"] = (
            cohort_df["juros_recebidos"] / cohort_df["valor_contratado"] * 100
        )
        cohort_df["ano_contratacao"] = cohort_df["ano_contratacao"].astype(str)

        interest_left, cohort_right = st.columns(2)

        with interest_left:
            st.markdown("**Juros recebidos ao longo do tempo**")
            cumulative_chart = alt.Chart(monthly_interest).mark_area(
                opacity=0.24,
                line={"color": "#482638", "strokeWidth": 2.5},
                color="#89556F",
            ).encode(
                x=alt.X(
                    "mes:T",
                    title=None,
                    axis=alt.Axis(format="%b %Y", labelAngle=-25),
                ),
                y=alt.Y(
                    "juros_acumulados:Q",
                    title="Juros acumulados (R$)",
                    axis=alt.Axis(format=",.0f"),
                ),
                tooltip=[
                    alt.Tooltip("mes:T", title="Mês", format="%b %Y"),
                    alt.Tooltip(
                        "juros_recebidos:Q",
                        title="Juros no mês",
                        format=",.2f",
                    ),
                    alt.Tooltip(
                        "juros_acumulados:Q",
                        title="Juros acumulados",
                        format=",.2f",
                    ),
                ],
            ).properties(height=300).configure(
                background="transparent"
            ).configure_view(stroke=None).configure_axis(
                labelColor="#51454C",
                titleColor="#51454C",
                gridColor="#E7DFE3",
                domainColor="#C9BBC2",
                tickColor="#C9BBC2",
                labelFont="Arial",
                titleFont="Arial",
            )
            st.altair_chart(cumulative_chart, use_container_width=True)

        with cohort_right:
            st.markdown("**Juros recebidos por safra**")
            cohort_chart = alt.Chart(cohort_df).mark_bar(
                cornerRadiusEnd=5,
                color="#70445B",
            ).encode(
                y=alt.Y(
                    "ano_contratacao:N",
                    title=None,
                    sort="ascending",
                    axis=alt.Axis(labelAngle=0),
                ),
                x=alt.X(
                    "juros_sobre_contratado_pct:Q",
                    title="Juros recebidos / valor contratado (%)",
                    axis=alt.Axis(format=".1f"),
                ),
                tooltip=[
                    alt.Tooltip("ano_contratacao:N", title="Safra"),
                    alt.Tooltip(
                        "juros_recebidos:Q",
                        title="Juros recebidos",
                        format=",.2f",
                    ),
                    alt.Tooltip(
                        "valor_contratado:Q",
                        title="Valor contratado",
                        format=",.2f",
                    ),
                    alt.Tooltip(
                        "juros_sobre_contratado_pct:Q",
                        title="Juros / contratado",
                        format=".2f",
                    ),
                ],
            ).properties(height=300).configure(
                background="transparent"
            ).configure_view(stroke=None).configure_axis(
                labelColor="#51454C",
                titleColor="#51454C",
                gridColor="#E7DFE3",
                domainColor="#C9BBC2",
                tickColor="#C9BBC2",
                labelFont="Arial",
                titleFont="Arial",
            )
            st.altair_chart(cohort_chart, use_container_width=True)

    else:
        st.info("Não há juros registrados nos pagamentos deste recorte.")

    st.divider()
    # -----------------------------------------------------
    # DETALHAMENTO
    # -----------------------------------------------------

    st.subheader("Detalhamento da carteira")

    display_columns = [
        "contract_id",
        "contract_date",
        "ano_contratacao",
        "qt_installment_total",
        "qt_installment_paid",
        "total_installment_amount",
        "open_installment_amount",
        "total_paid_amount",
        "days_late",
        "contract_situation",
    ]

    detail_df = filtered[
        [col for col in display_columns if col in filtered.columns]
    ].copy()

    detail_df = detail_df.rename(
        columns={
            "contract_id": "Contrato",
            "contract_date": "Data de contratação",
            "ano_contratacao": "Ano",
            "qt_installment_total": "Total de parcelas",
            "qt_installment_paid": "Parcelas pagas",
            "total_installment_amount": "Valor total",
            "open_installment_amount": "Saldo em aberto",
            "total_paid_amount": "Valor pago",
            "days_late": "Dias de atraso",
            "contract_situation": "Situação",
        }
    )

    st.dataframe(
        detail_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Data de contratação": st.column_config.DateColumn(
                format="DD/MM/YYYY"
            ),
            "Valor total": st.column_config.NumberColumn(
                format="R$ %.2f"
            ),
            "Saldo em aberto": st.column_config.NumberColumn(
                format="R$ %.2f"
            ),
            "Valor pago": st.column_config.NumberColumn(
                format="R$ %.2f"
            ),
        },
    )

    st.caption(
        "Fonte: snapshot estático | Transformações e regras de negócio: dbt | "
        "Data de referência dos indicadores: 31/12/2026."
    )

except Exception as e:
    st.error(
        "Não foi possível carregar o painel. "
        "Confira os arquivos CSV em data/streamlit."
    )
    st.exception(e)







