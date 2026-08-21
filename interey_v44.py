import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import html as html_lib
import math

st.set_page_config(page_title="INTEREY | Dashboard Corporativo", layout="wide")

# ---------- ESTILO ----------
st.markdown("""
<style>
:root{
    --interey-blue:#123E70;
    --interey-blue-2:#0B1F4D;
    --interey-red:#D52B24;
    --interey-graphite:#344648;
    --interey-bg:#F5F7FB;
    --interey-card:#FFFFFF;
    --interey-green:#118C7E;
    --interey-yellow:#D97706;
    --interey-gray:#64748B;
}
.stApp {background: linear-gradient(180deg, #F7F9FC 0%, #FFFFFF 42%);}
.block-container {padding-top: 1.0rem; padding-bottom: 2rem; max-width: 1520px;}
[data-testid="stSidebar"] {background: #EEF3F8;}

/* Header INTEREY */
.hero-wrap{
    background: transparent;
    border: none;
    border-radius: 0;
    padding: 6px 0 14px 0;
    box-shadow: none;
    margin-top: 0;
    margin-bottom: 10px;
}
.hero-title{font-size:2.25rem; font-weight:900; color:var(--interey-blue-2); letter-spacing:-.045em; line-height:1.02;}
.hero-kicker{font-size:.82rem; font-weight:800; color:var(--interey-red); letter-spacing:.13em; text-transform:uppercase; margin-bottom:4px;}
.hero-subtitle{font-size:1.04rem; color:var(--interey-graphite); margin-top:4px;}
.hero-pill{background:#FFFFFF; border:1px solid rgba(18,62,112,.16); border-radius:999px; padding:8px 12px; color:#334155; font-size:.82rem; display:inline-block; margin-top:8px;}
.hero-date{text-align:right; color:#475569; font-size:.83rem; padding-top:6px;}
.logo-box-premium img{max-height:74px; object-fit:contain;}

/* Cards */
.kpi-card {
    background: linear-gradient(135deg, var(--interey-blue-2) 0%, var(--interey-blue) 100%);
    color: white;
    border-radius: 18px;
    padding: 16px 18px;
    box-shadow: 0 8px 22px rgba(11,31,77,.14);
    height: 136px;
    min-height: 136px;
    max-height: 136px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    overflow: hidden;
    box-sizing: border-box;
    border: 1px solid rgba(255,255,255,.18);
}
.kpi-card.green {background: linear-gradient(135deg, #0F766E 0%, var(--interey-green) 100%);}
.kpi-card.gray {background: linear-gradient(135deg, #334155 0%, #64748B 100%);}
.kpi-card.red {background: linear-gradient(135deg, #991B1B 0%, var(--interey-red) 100%);}
.kpi-card.yellow {background: linear-gradient(135deg, #92400E 0%, var(--interey-yellow) 100%);}
.kpi-card.orange {background: linear-gradient(135deg, #C2410C 0%, #EA580C 100%);}
.kpi-card.orange {background: linear-gradient(135deg, #9A3412 0%, #EA580C 100%);}
.kpi-label {font-size: .82rem; opacity: .94; line-height: 1.15; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-weight:700;}
.kpi-value {font-size: 1.62rem; font-weight: 900; margin-top: .10rem; line-height: 1.12; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; letter-spacing:-.02em;}
.kpi-sub {font-size: .72rem; opacity: .88; margin-top: .10rem; line-height: 1.22; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;}
.kpi-spacer{height:14px;}

.section-title {font-size: 1.18rem; font-weight: 850; color: var(--interey-blue-2); margin-top: 1.0rem; margin-bottom: .62rem; letter-spacing:-.01em;}
.small-note {font-size: .82rem; color: #6B7280;}
.exec-band {background: #FFFFFF; border: 1px solid rgba(18,62,112,.12); border-radius: 16px; padding: 10px 14px; margin-bottom: .9rem; box-shadow:0 4px 12px rgba(15,23,42,.04);}
.trend-note {font-size: .82rem; color: #475569; margin-top: .55rem; background: #F8FAFC; border-left: 4px solid var(--interey-blue); padding: 9px 11px; border-radius: 10px;}

/* Radar INTEREY 2.0 */
.radar-card{
    background:linear-gradient(135deg,#071A33 0%, #123E70 55%, #1D5C92 100%);
    border:1px solid rgba(255,255,255,.18);
    border-radius:24px;
    padding:20px 22px;
    margin:12px 0 18px 0;
    box-shadow:0 16px 36px rgba(11,31,77,.18);
    color:#FFFFFF;
    overflow:hidden;
    position:relative;
}
.radar-card:before{content:""; position:absolute; right:-70px; top:-90px; width:260px; height:260px; border-radius:50%; background:rgba(255,255,255,.08);}
.radar-card:after{content:""; position:absolute; right:34px; bottom:-78px; width:180px; height:180px; border-radius:50%; background:rgba(213,43,36,.13);}
.radar-head{display:flex; justify-content:space-between; gap:18px; align-items:flex-start; position:relative; z-index:2; margin-bottom:15px;}
.radar-title{font-size:1.32rem; font-weight:950; letter-spacing:-.02em; margin-bottom:3px; color:#FFFFFF;}
.radar-subtitle{font-size:.86rem; color:rgba(255,255,255,.78); line-height:1.32;}
.radar-badge{background:rgba(255,255,255,.12); border:1px solid rgba(255,255,255,.24); border-radius:999px; padding:8px 12px; font-size:.78rem; font-weight:850; color:#FFFFFF; white-space:nowrap;}
.radar2-grid{display:grid; grid-template-columns:1.25fr repeat(3, minmax(0, .9fr)); gap:12px; position:relative; z-index:2;}
.radar2-main{background:rgba(255,255,255,.12); border:1px solid rgba(255,255,255,.22); border-radius:18px; padding:15px 16px; min-height:142px;}
.radar2-main-label{font-size:.76rem; font-weight:850; text-transform:uppercase; letter-spacing:.08em; color:rgba(255,255,255,.72);}
.radar2-main-value{font-size:1.45rem; line-height:1.12; font-weight:950; margin-top:7px; color:#FFFFFF; letter-spacing:-.025em;}
.radar2-main-sub{font-size:.83rem; line-height:1.33; color:rgba(255,255,255,.78); margin-top:9px;}
.radar2-tile{background:#FFFFFF; color:#0F172A; border-radius:18px; padding:14px 14px; box-shadow:0 10px 24px rgba(15,23,42,.13); min-height:142px; border-top:5px solid var(--interey-blue);}
.radar2-tile.green{border-top-color:var(--interey-green);}
.radar2-tile.red{border-top-color:var(--interey-red);}
.radar2-tile.yellow{border-top-color:var(--interey-yellow);}
.radar2-label{font-size:.74rem; font-weight:900; color:#64748B; text-transform:uppercase; letter-spacing:.06em;}
.radar2-value{font-size:1.22rem; font-weight:950; color:#0B1F4D; margin-top:6px; line-height:1.12;}
.radar2-text{font-size:.81rem; color:#475569; line-height:1.30; margin-top:8px;}
.radar2-list{margin:8px 0 0 0; padding-left:0; list-style:none;}
.radar2-list li{font-size:.80rem; color:#334155; line-height:1.32; margin:5px 0;}
.radar2-list li:before{content:"•"; color:var(--interey-blue); font-weight:950; margin-right:7px;}
.radar2-tile.green .radar2-list li:before{color:var(--interey-green);}
.radar2-tile.red .radar2-list li:before{color:var(--interey-red);}
.radar2-tile.yellow .radar2-list li:before{color:var(--interey-yellow);}
@media (max-width: 1200px){.radar2-grid{grid-template-columns:1fr 1fr;}}
@media (max-width: 760px){.radar-head{display:block;} .radar-badge{display:inline-block;margin-top:10px;} .radar2-grid{grid-template-columns:1fr;}}

/* Radar INTEREY 4.0 · Executive Command Bar */
.radar-exec{
    background:#FFFFFF;
    border:1px solid #DDE5EE;
    border-radius:20px;
    overflow:hidden;
    margin:12px 0 18px 0;
    box-shadow:0 10px 28px rgba(15,23,42,.07);
}
.radar-exec-top{
    background:linear-gradient(135deg,#0B1F4D 0%,#123E70 72%,#1C568D 100%);
    color:#FFFFFF;
    padding:14px 18px;
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:18px;
}
.radar-exec-brand{
    display:flex;
    align-items:center;
    gap:10px;
}
.radar-exec-icon{
    width:32px;
    height:32px;
    border-radius:10px;
    background:rgba(255,255,255,.12);
    border:1px solid rgba(255,255,255,.18);
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:1rem;
}
.radar-exec-title{
    font-size:1.08rem;
    font-weight:950;
    letter-spacing:-.02em;
    color:#FFFFFF;
}
.radar-exec-kicker{
    font-size:.68rem;
    font-weight:800;
    letter-spacing:.10em;
    text-transform:uppercase;
    color:rgba(255,255,255,.68);
    margin-top:1px;
}
.radar-exec-status{
    border-radius:999px;
    padding:7px 11px;
    font-size:.73rem;
    font-weight:900;
    letter-spacing:.02em;
    white-space:nowrap;
    border:1px solid rgba(255,255,255,.24);
    background:rgba(255,255,255,.10);
    color:#FFFFFF;
}
.radar-exec-summary{
    padding:15px 18px 13px 18px;
    border-bottom:1px solid #E7EDF4;
    background:linear-gradient(180deg,#FFFFFF 0%,#FBFCFE 100%);
}
.radar-exec-summary-label{
    font-size:.68rem;
    color:#64748B;
    text-transform:uppercase;
    font-weight:900;
    letter-spacing:.10em;
    margin-bottom:5px;
}
.radar-exec-summary-title{
    color:#0B1F4D;
    font-size:1.23rem;
    line-height:1.20;
    font-weight:950;
    letter-spacing:-.025em;
}
.radar-exec-summary-sub{
    color:#64748B;
    font-size:.79rem;
    line-height:1.35;
    margin-top:5px;
}
.radar-exec-grid{
    display:grid;
    grid-template-columns:repeat(4,minmax(0,1fr));
    background:#FFFFFF;
}
.radar-exec-metric{
    min-height:108px;
    padding:14px 17px 13px 17px;
    border-right:1px solid #E7EDF4;
    position:relative;
}
.radar-exec-metric:last-child{border-right:none;}
.radar-exec-metric:before{
    content:"";
    position:absolute;
    top:0;
    left:17px;
    right:17px;
    height:3px;
    border-radius:0 0 4px 4px;
    background:#123E70;
}
.radar-exec-metric.good:before{background:#118C7E;}
.radar-exec-metric.warn:before{background:#D97706;}
.radar-exec-metric.bad:before{background:#D52B24;}
.radar-exec-metric.neutral:before{background:#64748B;}
.radar-exec-label{
    color:#64748B;
    font-size:.69rem;
    font-weight:900;
    text-transform:uppercase;
    letter-spacing:.075em;
    margin-top:3px;
}
.radar-exec-value{
    color:#0B1F4D;
    font-size:1.45rem;
    font-weight:950;
    letter-spacing:-.035em;
    line-height:1.08;
    margin-top:8px;
}
.radar-exec-meta{
    color:#64748B;
    font-size:.74rem;
    line-height:1.28;
    margin-top:6px;
}
.radar-exec-signal{
    display:inline-flex;
    align-items:center;
    gap:5px;
}
.radar-exec-dot{
    width:7px;
    height:7px;
    border-radius:50%;
    display:inline-block;
    background:#64748B;
}
.radar-exec-dot.good{background:#118C7E;}
.radar-exec-dot.warn{background:#D97706;}
.radar-exec-dot.bad{background:#D52B24;}
.radar-exec-action{
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:18px;
    padding:12px 18px;
    background:#F6F9FC;
    border-top:1px solid #E7EDF4;
}
.radar-exec-action-left{
    display:flex;
    align-items:center;
    gap:10px;
    min-width:0;
}
.radar-exec-action-icon{
    width:30px;
    height:30px;
    border-radius:9px;
    background:#E8F0FA;
    color:#123E70;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:.92rem;
    flex:0 0 auto;
}
.radar-exec-action-label{
    color:#64748B;
    font-size:.66rem;
    font-weight:900;
    text-transform:uppercase;
    letter-spacing:.09em;
}
.radar-exec-action-text{
    color:#1E293B;
    font-size:.79rem;
    font-weight:750;
    margin-top:2px;
}
.radar-exec-action-value{
    color:#0B1F4D;
    font-size:1.28rem;
    font-weight:950;
    letter-spacing:-.03em;
    white-space:nowrap;
}
@media (max-width:1000px){
    .radar-exec-grid{grid-template-columns:repeat(2,minmax(0,1fr));}
    .radar-exec-metric:nth-child(2){border-right:none;}
    .radar-exec-metric:nth-child(-n+2){border-bottom:1px solid #E7EDF4;}
}
@media (max-width:640px){
    .radar-exec-top{display:block;}
    .radar-exec-status{display:inline-block;margin-top:10px;}
    .radar-exec-grid{grid-template-columns:1fr;}
    .radar-exec-metric{border-right:none;border-bottom:1px solid #E7EDF4;}
    .radar-exec-metric:last-child{border-bottom:none;}
    .radar-exec-action{align-items:flex-start;flex-direction:column;}
    .radar-exec-action-value{padding-left:40px;}
}

/* KPI Cards 2.0 · Executive refinement */
.kpi-card{
    --kpi-accent:#123E70;
    background:linear-gradient(180deg,#FFFFFF 0%,#FBFCFE 100%) !important;
    color:#0B1F4D !important;
    border:1px solid #DDE5EE !important;
    border-top:4px solid var(--kpi-accent) !important;
    border-radius:16px !important;
    padding:14px 16px 13px 16px !important;
    box-shadow:0 7px 20px rgba(15,23,42,.07) !important;
    height:124px !important;
    min-height:124px !important;
    max-height:124px !important;
    position:relative;
    transition:box-shadow .16s ease,border-color .16s ease;
}
.kpi-card:hover{
    box-shadow:0 10px 24px rgba(15,23,42,.10) !important;
    border-color:#CBD6E3 !important;
}
.kpi-card.green{--kpi-accent:#118C7E;}
.kpi-card.gray{--kpi-accent:#64748B;}
.kpi-card.red{--kpi-accent:#D52B24;}
.kpi-card.yellow{--kpi-accent:#D97706;}
.kpi-card.orange{--kpi-accent:#EA580C;}

.kpi-card .kpi-label{
    color:#5F6F82 !important;
    opacity:1 !important;
    font-size:.72rem !important;
    font-weight:900 !important;
    letter-spacing:.015em;
    line-height:1.18 !important;
}
.kpi-card .kpi-value{
    color:#0B1F4D !important;
    font-size:1.48rem !important;
    font-weight:950 !important;
    line-height:1.08 !important;
    letter-spacing:-.035em !important;
    margin-top:.14rem !important;
}
.kpi-card .kpi-sub{
    color:#718096 !important;
    opacity:1 !important;
    font-size:.70rem !important;
    line-height:1.25 !important;
    margin-top:.16rem !important;
}
.kpi-card.red .kpi-value{color:#B42318 !important;}
.kpi-card.green .kpi-value{color:#0F766E !important;}
.kpi-card.yellow .kpi-value{color:#B45309 !important;}
.kpi-card.orange .kpi-value{color:#C2410C !important;}

.kpi-card:after{
    content:"";
    position:absolute;
    right:14px;
    top:14px;
    width:7px;
    height:7px;
    border-radius:50%;
    background:var(--kpi-accent);
    box-shadow:0 0 0 4px rgba(148,163,184,.10);
}
.kpi-spacer{height:12px;}

@media (max-width:900px){
    .kpi-card{
        height:120px !important;
        min-height:120px !important;
        max-height:120px !important;
    }
}

/* Backlog 2.0 · Executive refinement */
.backlog-exec{
    background:#FFFFFF;
    border:1px solid #DDE5EE;
    border-radius:20px;
    overflow:hidden;
    margin:12px 0 16px 0;
    box-shadow:0 10px 28px rgba(15,23,42,.07);
}
.backlog-exec-top{
    background:linear-gradient(135deg,#0B1F4D 0%,#123E70 72%,#1C568D 100%);
    color:#FFFFFF;
    padding:13px 18px;
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:16px;
}
.backlog-exec-title{
    font-size:1.08rem;
    font-weight:950;
    letter-spacing:-.02em;
}
.backlog-exec-kicker{
    font-size:.67rem;
    font-weight:850;
    letter-spacing:.10em;
    text-transform:uppercase;
    color:rgba(255,255,255,.68);
    margin-top:1px;
}
.backlog-exec-status{
    border-radius:999px;
    padding:7px 11px;
    font-size:.72rem;
    font-weight:900;
    white-space:nowrap;
    border:1px solid rgba(255,255,255,.24);
    background:rgba(255,255,255,.10);
}
.backlog-exec-summary{
    padding:15px 18px 13px 18px;
    border-bottom:1px solid #E7EDF4;
    background:linear-gradient(180deg,#FFFFFF 0%,#FBFCFE 100%);
}
.backlog-exec-summary-label{
    font-size:.67rem;
    color:#64748B;
    text-transform:uppercase;
    font-weight:900;
    letter-spacing:.10em;
}
.backlog-exec-summary-title{
    color:#0B1F4D;
    font-size:1.22rem;
    line-height:1.18;
    font-weight:950;
    letter-spacing:-.025em;
    margin-top:5px;
}
.backlog-exec-summary-sub{
    color:#64748B;
    font-size:.78rem;
    line-height:1.35;
    margin-top:5px;
}
.backlog-exec-grid{
    display:grid;
    grid-template-columns:repeat(4,minmax(0,1fr));
}
.backlog-exec-metric{
    min-height:108px;
    padding:14px 17px 13px 17px;
    border-right:1px solid #E7EDF4;
    position:relative;
}
.backlog-exec-metric:last-child{border-right:none;}
.backlog-exec-metric:before{
    content:"";
    position:absolute;
    left:17px;
    right:17px;
    top:0;
    height:3px;
    border-radius:0 0 4px 4px;
    background:#64748B;
}
.backlog-exec-metric.good:before{background:#118C7E;}
.backlog-exec-metric.warn:before{background:#D97706;}
.backlog-exec-metric.bad:before{background:#D52B24;}
.backlog-exec-metric.blue:before{background:#123E70;}
.backlog-exec-label{
    color:#64748B;
    font-size:.68rem;
    font-weight:900;
    text-transform:uppercase;
    letter-spacing:.07em;
    margin-top:3px;
}
.backlog-exec-value{
    color:#0B1F4D;
    font-size:1.43rem;
    font-weight:950;
    letter-spacing:-.035em;
    line-height:1.08;
    margin-top:8px;
}
.backlog-exec-metric.good .backlog-exec-value{color:#0F766E;}
.backlog-exec-metric.warn .backlog-exec-value{color:#B45309;}
.backlog-exec-metric.bad .backlog-exec-value{color:#B42318;}
.backlog-exec-meta{
    color:#64748B;
    font-size:.73rem;
    line-height:1.28;
    margin-top:6px;
}
.backlog-exec-action{
    display:flex;
    justify-content:space-between;
    align-items:center;
    gap:18px;
    padding:12px 18px;
    background:#F6F9FC;
    border-top:1px solid #E7EDF4;
}
.backlog-exec-action-label{
    color:#64748B;
    font-size:.66rem;
    font-weight:900;
    text-transform:uppercase;
    letter-spacing:.09em;
}
.backlog-exec-action-text{
    color:#1E293B;
    font-size:.79rem;
    font-weight:750;
    margin-top:2px;
}
.backlog-exec-action-value{
    color:#0B1F4D;
    font-size:1.25rem;
    font-weight:950;
    letter-spacing:-.03em;
    white-space:nowrap;
}

/* Riesgo financiero: alerta ejecutiva, no bloque rojo completo */
.backlog-risk-strip{
    display:grid;
    grid-template-columns:1.25fr repeat(3,minmax(0,.7fr));
    align-items:center;
    gap:0;
    background:#FFFFFF;
    border:1px solid #E3E8EF;
    border-left:5px solid #D52B24;
    border-radius:15px;
    margin:12px 0 16px 0;
    overflow:hidden;
    box-shadow:0 6px 18px rgba(15,23,42,.05);
}
.backlog-risk-main{
    padding:12px 15px;
}
.backlog-risk-label{
    color:#B42318;
    font-size:.67rem;
    font-weight:950;
    letter-spacing:.08em;
    text-transform:uppercase;
}
.backlog-risk-title{
    color:#0B1F4D;
    font-size:.91rem;
    font-weight:900;
    margin-top:4px;
}
.backlog-risk-cell{
    padding:11px 14px;
    border-left:1px solid #E7EDF4;
}
.backlog-risk-cell-label{
    color:#64748B;
    font-size:.64rem;
    font-weight:850;
    text-transform:uppercase;
    letter-spacing:.07em;
}
.backlog-risk-cell-value{
    color:#0B1F4D;
    font-size:1rem;
    font-weight:950;
    margin-top:4px;
}
.backlog-risk-cell.bad .backlog-risk-cell-value{color:#B42318;}

.backlog-coverage-note{
    font-size:.73rem;
    color:#64748B;
    margin-top:7px;
    line-height:1.35;
}

@media (max-width:1000px){
    .backlog-exec-grid{grid-template-columns:repeat(2,minmax(0,1fr));}
    .backlog-exec-metric:nth-child(2){border-right:none;}
    .backlog-exec-metric:nth-child(-n+2){border-bottom:1px solid #E7EDF4;}
    .backlog-risk-strip{grid-template-columns:1fr 1fr;}
    .backlog-risk-main{grid-column:1/-1;border-bottom:1px solid #E7EDF4;}
}
@media (max-width:640px){
    .backlog-exec-top{display:block;}
    .backlog-exec-status{display:inline-block;margin-top:9px;}
    .backlog-exec-grid{grid-template-columns:1fr;}
    .backlog-exec-metric{border-right:none;border-bottom:1px solid #E7EDF4;}
    .backlog-exec-action{align-items:flex-start;flex-direction:column;}
    .backlog-risk-strip{grid-template-columns:1fr;}
    .backlog-risk-main{grid-column:auto;}
    .backlog-risk-cell{border-left:none;border-top:1px solid #E7EDF4;}
}

/* Backlog · Master Detail */
.backlog-master-summary{
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:14px;
    padding:9px 12px;
    background:#F7F9FC;
    border:1px solid #E2E8F0;
    border-radius:12px;
    margin:8px 0 9px 0;
}
.backlog-master-summary-main{
    color:#0B1F4D;
    font-size:.80rem;
    font-weight:900;
}
.backlog-master-summary-sub{
    color:#64748B;
    font-size:.72rem;
    text-align:right;
}
.backlog-master-wrap{
    border:1px solid #E1E7EF;
    border-radius:15px;
    overflow:auto;
    max-height:520px;
    background:#FFFFFF;
    box-shadow:0 5px 16px rgba(15,23,42,.04);
}
.backlog-master-table{
    width:100%;
    border-collapse:separate;
    border-spacing:0;
    table-layout:fixed;
    color:#243244;
    font-size:.76rem;
}
.backlog-master-table th{
    position:sticky;
    top:0;
    z-index:2;
    background:#F6F8FB;
    color:#5F6F82;
    font-size:.67rem;
    font-weight:900;
    letter-spacing:.055em;
    text-transform:uppercase;
    padding:9px 10px;
    text-align:left;
    border-bottom:1px solid #DCE4ED;
}
.backlog-master-table td{
    padding:9px 10px;
    border-bottom:1px solid #EDF1F5;
    vertical-align:middle;
    background:#FFFFFF;
}
.backlog-master-table tr:last-child td{border-bottom:none;}
.backlog-master-table tr:hover td{background:#FAFBFD;}
.backlog-master-table .col-age{width:8%;}
.backlog-master-table .col-number{width:9%;text-align:center;}
.backlog-master-table .col-client{width:22%;}
.backlog-master-table .col-project{width:35%;}
.backlog-master-table .col-days{width:10%;text-align:right;}
.backlog-master-table .col-amount{width:16%;text-align:right;}
.backlog-project-two-lines{
    display:-webkit-box;
    -webkit-line-clamp:2;
    -webkit-box-orient:vertical;
    overflow:hidden;
    white-space:normal;
    line-height:1.30;
    color:#334155;
}
.backlog-client-cell{
    font-weight:850;
    color:#0B1F4D;
    line-height:1.25;
    white-space:normal;
}
.age-pill{
    display:inline-block;
    border-radius:999px;
    padding:4px 7px;
    font-size:.65rem;
    font-weight:900;
    white-space:nowrap;
    background:#EEF2F7;
    color:#526174;
}
.age-pill.good{background:#EAF7F4;color:#0F766E;}
.age-pill.warn{background:#FFF7E6;color:#A65E00;}
.age-pill.attn{background:#FFF2E8;color:#C35C17;}
.age-pill.bad{background:#FDECEC;color:#B42318;}

.backlog-detail-panel{
    margin-top:10px;
    background:#FFFFFF;
    border:1px solid #DDE5EE;
    border-left:4px solid #123E70;
    border-radius:14px;
    padding:13px 15px 14px 15px;
    box-shadow:0 5px 16px rgba(15,23,42,.04);
}
.backlog-detail-panel.good{border-left-color:#118C7E;}
.backlog-detail-panel.warn{border-left-color:#D97706;}
.backlog-detail-panel.attn{border-left-color:#EA580C;}
.backlog-detail-panel.bad{border-left-color:#D52B24;}
.backlog-detail-kicker{
    color:#64748B;
    font-size:.66rem;
    font-weight:900;
    letter-spacing:.08em;
    text-transform:uppercase;
}
.backlog-detail-title{
    color:#0B1F4D;
    font-size:1rem;
    font-weight:950;
    margin-top:4px;
}
.backlog-detail-project{
    color:#475569;
    font-size:.78rem;
    line-height:1.40;
    margin-top:5px;
}
.backlog-detail-grid{
    display:grid;
    grid-template-columns:repeat(5,minmax(0,1fr));
    gap:0;
    margin-top:12px;
    border-top:1px solid #E8EDF3;
}
.backlog-detail-item{
    padding:10px 12px 0 0;
}
.backlog-detail-item + .backlog-detail-item{
    padding-left:12px;
    border-left:1px solid #E8EDF3;
}
.backlog-detail-label{
    color:#64748B;
    font-size:.63rem;
    font-weight:900;
    letter-spacing:.06em;
    text-transform:uppercase;
}
.backlog-detail-value{
    color:#0B1F4D;
    font-size:.86rem;
    font-weight:900;
    margin-top:3px;
}
@media(max-width:760px){
    .backlog-master-summary{display:block;}
    .backlog-master-summary-sub{text-align:left;margin-top:3px;}
    .backlog-master-table .col-project{width:31%;}
    .backlog-detail-grid{grid-template-columns:1fr 1fr;}
    .backlog-detail-item:nth-child(3){border-left:none;padding-left:0;}
}

/* Desempeño Comercial 2.0 */
.team-exec-strip{
    display:grid;
    grid-template-columns:repeat(4,minmax(0,1fr));
    background:#FFFFFF;
    border:1px solid #DDE5EE;
    border-radius:16px;
    overflow:hidden;
    margin:8px 0 14px 0;
    box-shadow:0 6px 18px rgba(15,23,42,.05);
}
.team-exec-cell{
    padding:12px 14px;
    border-right:1px solid #E7EDF4;
    position:relative;
}
.team-exec-cell:last-child{border-right:none;}
.team-exec-cell:before{
    content:"";
    position:absolute;
    top:0;
    left:14px;
    right:14px;
    height:3px;
    border-radius:0 0 4px 4px;
    background:#123E70;
}
.team-exec-cell.good:before{background:#118C7E;}
.team-exec-cell.warn:before{background:#D97706;}
.team-exec-cell.bad:before{background:#D52B24;}
.team-exec-label{
    color:#64748B;
    font-size:.64rem;
    font-weight:900;
    text-transform:uppercase;
    letter-spacing:.07em;
    margin-top:3px;
}
.team-exec-value{
    color:#0B1F4D;
    font-size:1.05rem;
    font-weight:950;
    margin-top:6px;
    line-height:1.16;
}
.team-exec-sub{
    color:#718096;
    font-size:.69rem;
    margin-top:4px;
    line-height:1.25;
}

.team-ranking{
    background:#FFFFFF;
    border:1px solid #DDE5EE;
    border-radius:16px;
    overflow:hidden;
    box-shadow:0 6px 18px rgba(15,23,42,.05);
    margin:8px 0 16px 0;
}
.team-ranking-head,
.team-ranking-row{
    display:grid;
    grid-template-columns:42px minmax(150px,1.25fr) minmax(110px,.85fr) minmax(190px,1.25fr) minmax(120px,.85fr) minmax(105px,.75fr);
    align-items:center;
}
.team-ranking-head{
    background:#F6F8FB;
    color:#64748B;
    border-bottom:1px solid #E1E7EF;
    font-size:.64rem;
    font-weight:900;
    letter-spacing:.06em;
    text-transform:uppercase;
}
.team-ranking-head > div{padding:9px 10px;}
.team-ranking-row{
    border-bottom:1px solid #EDF1F5;
    min-height:66px;
}
.team-ranking-row:last-child{border-bottom:none;}
.team-ranking-row:hover{background:#FBFCFE;}
.team-ranking-row > div{padding:10px;}
.team-rank-number{
    color:#94A3B8;
    font-size:.78rem;
    font-weight:900;
    text-align:center;
}
.team-rank-name{
    color:#0B1F4D;
    font-size:.79rem;
    font-weight:900;
    line-height:1.20;
}
.team-rank-sales{
    color:#0B1F4D;
    font-size:.83rem;
    font-weight:950;
}
.team-rank-secondary{
    color:#64748B;
    font-size:.67rem;
    margin-top:2px;
}
.team-progress-top{
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:8px;
    font-size:.69rem;
    color:#64748B;
    margin-bottom:5px;
}
.team-progress-value{
    color:#0B1F4D;
    font-weight:900;
}
.team-progress-track{
    height:8px;
    background:#EDF1F5;
    border-radius:999px;
    overflow:hidden;
}
.team-progress-fill{
    height:8px;
    border-radius:999px;
    background:#123E70;
}
.team-progress-fill.good{background:#118C7E;}
.team-progress-fill.warn{background:#D97706;}
.team-progress-fill.bad{background:#D52B24;}
.team-status{
    display:inline-block;
    border-radius:999px;
    padding:5px 8px;
    font-size:.65rem;
    font-weight:900;
    background:#F1F5F9;
    color:#526174;
    white-space:nowrap;
}
.team-status.good{background:#EAF7F4;color:#0F766E;}
.team-status.warn{background:#FFF7E6;color:#A65E00;}
.team-status.bad{background:#FDECEC;color:#B42318;}

.team-pulse-wrap{
    overflow-x:auto;
    border:1px solid #DDE5EE;
    border-radius:15px;
    background:#FFFFFF;
    box-shadow:0 5px 16px rgba(15,23,42,.04);
    margin:8px 0 16px 0;
}
.team-pulse{
    width:100%;
    border-collapse:collapse;
    font-size:.72rem;
}
.team-pulse th{
    background:#F6F8FB;
    color:#64748B;
    font-size:.63rem;
    font-weight:900;
    text-transform:uppercase;
    letter-spacing:.05em;
    padding:8px 9px;
    border-bottom:1px solid #E1E7EF;
    text-align:center;
}
.team-pulse th:first-child{text-align:left;}
.team-pulse td{
    padding:8px 9px;
    border-bottom:1px solid #EDF1F5;
    text-align:center;
    color:#475569;
}
.team-pulse tr:last-child td{border-bottom:none;}
.team-pulse td:first-child{
    text-align:left;
    color:#0B1F4D;
    font-weight:850;
    white-space:nowrap;
}
.pulse-value{
    display:inline-flex;
    align-items:center;
    gap:5px;
    font-weight:850;
}
.pulse-dot{
    width:6px;
    height:6px;
    border-radius:50%;
    background:#94A3B8;
}
.pulse-dot.good{background:#118C7E;}
.pulse-dot.warn{background:#D97706;}
.pulse-dot.bad{background:#D52B24;}
.pulse-dot.none{background:#CBD5E1;}

@media(max-width:1050px){
    .team-exec-strip{grid-template-columns:repeat(2,minmax(0,1fr));}
    .team-exec-cell:nth-child(2){border-right:none;}
    .team-exec-cell:nth-child(-n+2){border-bottom:1px solid #E7EDF4;}
}
@media(max-width:820px){
    .team-ranking-head{display:none;}
    .team-ranking-row{
        grid-template-columns:34px 1.3fr 1fr;
        gap:0;
    }
    .team-ranking-row > div:nth-child(4),
    .team-ranking-row > div:nth-child(5),
    .team-ranking-row > div:nth-child(6){
        grid-column:2/4;
    }
}


/* Executive summary V43 */
.exec-summary-wrap{
    background: linear-gradient(135deg,#FFFFFF 0%,#F8FAFC 100%);
    border:1px solid rgba(18,62,112,.14);
    border-radius:22px;
    padding:18px 20px;
    margin:14px 0 18px 0;
    box-shadow:0 12px 30px rgba(15,23,42,.07);
}
.exec-summary-title{font-size:1.22rem;font-weight:950;color:var(--interey-blue-2);letter-spacing:-.02em;margin-bottom:4px;}
.exec-summary-sub{font-size:.85rem;color:#64748B;margin-bottom:14px;}
.exec-progress-card{
    background:linear-gradient(135deg,var(--interey-blue-2) 0%,var(--interey-blue) 100%);
    border-radius:20px;
    padding:18px 20px;
    color:#FFFFFF;
    box-shadow:0 10px 26px rgba(11,31,77,.16);
    overflow:hidden;
    position:relative;
}
.exec-progress-card:after{content:"";position:absolute;right:-40px;top:-60px;width:170px;height:170px;background:rgba(255,255,255,.08);border-radius:50%;}
.exec-progress-head{display:flex;justify-content:space-between;gap:12px;align-items:flex-end;position:relative;z-index:2;}
.exec-progress-label{font-size:.78rem;text-transform:uppercase;letter-spacing:.08em;font-weight:900;color:rgba(255,255,255,.75);}
.exec-progress-value{font-size:2.35rem;font-weight:950;letter-spacing:-.05em;line-height:1;}
.exec-progress-status{font-size:.88rem;font-weight:850;color:rgba(255,255,255,.88);text-align:right;}
.exec-progress-track{height:16px;background:rgba(255,255,255,.18);border-radius:999px;margin-top:16px;overflow:hidden;position:relative;z-index:2;}
.exec-progress-fill{height:16px;border-radius:999px;background:linear-gradient(90deg,#FFFFFF 0%,#DCEBFF 100%);}
.exec-progress-foot{font-size:.80rem;color:rgba(255,255,255,.78);margin-top:10px;position:relative;z-index:2;}
.exec-insights-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-top:14px;}
.exec-insight{background:#FFFFFF;border:1px solid #E2E8F0;border-radius:18px;padding:14px 14px;min-height:112px;box-shadow:0 8px 22px rgba(15,23,42,.05);border-left:5px solid var(--interey-blue);}
.exec-insight.green{border-left-color:var(--interey-green);} .exec-insight.red{border-left-color:var(--interey-red);} .exec-insight.yellow{border-left-color:var(--interey-yellow);} .exec-insight.gray{border-left-color:var(--interey-gray);}
.exec-insight-label{font-size:.74rem;text-transform:uppercase;letter-spacing:.06em;color:#64748B;font-weight:900;}
.exec-insight-value{font-size:1.05rem;line-height:1.20;font-weight:950;color:#0B1F4D;margin-top:7px;}
.exec-insight-text{font-size:.80rem;line-height:1.30;color:#475569;margin-top:7px;}
@media (max-width:1200px){.exec-insights-grid{grid-template-columns:repeat(2,minmax(0,1fr));}}
@media (max-width:760px){.exec-insights-grid{grid-template-columns:1fr;}}


/* Executive view selector */
.view-selector-card{
    background:linear-gradient(135deg,#FFFFFF 0%,#F8FAFC 100%);
    border:1px solid rgba(18,62,112,.14);
    border-radius:18px;
    padding:14px 18px 10px 18px;
    margin:12px 0 16px 0;
    box-shadow:0 8px 22px rgba(15,23,42,.05);
}
.view-selector-title{font-size:1.05rem;font-weight:900;color:var(--interey-blue-2);margin-bottom:2px;}
.view-selector-sub{font-size:.80rem;color:#64748B;margin-bottom:8px;}
div[role="radiogroup"] label{
    background:#FFFFFF;
    border:1px solid #D8E2EC;
    border-radius:999px;
    padding:8px 13px;
    margin-right:8px;
    box-shadow:0 3px 10px rgba(15,23,42,.04);
}
div[role="radiogroup"] label:hover{border-color:var(--interey-blue); transform: translateY(-1px); transition:.15s ease;}
div[role="radiogroup"] label:has(input:checked){
    background:linear-gradient(135deg, var(--interey-blue-2) 0%, var(--interey-blue) 100%);
    color:#FFFFFF !important;
    border-color:var(--interey-blue-2);
    box-shadow:0 8px 18px rgba(18,62,112,.20);
}
div[role="radiogroup"] label:has(input:checked) p{color:#FFFFFF !important; font-weight:900;}

/* Streamlit tabs */
button[data-baseweb="tab"]{font-weight:700;}
button[data-baseweb="tab"][aria-selected="true"]{color:var(--interey-red);}



/* Premium tables */
.premium-table-wrap{
    background:#FFFFFF;
    border:1px solid rgba(18,62,112,.12);
    border-radius:16px;
    padding:10px 10px 8px 10px;
    box-shadow:0 8px 20px rgba(15,23,42,.05);
    overflow-x:auto;
    margin:8px 0 18px 0;
}
.premium-table{
    width:100%;
    border-collapse:separate;
    border-spacing:0;
    font-size:.82rem;
    color:#1F2937;
}
.premium-table th{
    background:linear-gradient(135deg, var(--interey-blue-2) 0%, var(--interey-blue) 100%);
    color:#FFFFFF;
    padding:9px 10px;
    text-align:right;
    font-weight:850;
    border-right:1px solid rgba(255,255,255,.16);
    white-space:nowrap;
}
.premium-table th:first-child{
    text-align:left;
    border-top-left-radius:10px;
}
.premium-table th:last-child{
    border-top-right-radius:10px;
    border-right:none;
}
.premium-table td{
    padding:8px 10px;
    text-align:right;
    border-bottom:1px solid #E5EAF0;
    white-space:nowrap;
}
.premium-table td:first-child{
    text-align:left;
    font-weight:800;
    color:var(--interey-blue-2);
}
.premium-table tr:nth-child(even) td{background:#F8FAFC;}
.premium-table tr.highlight-row td{background:#EEF6FF; font-weight:850;}
.premium-table tr.risk-row td{background:#FFF7F7;}
.premium-table tr.warn-row td{background:#FFFBEB;}
.premium-table tr.attention-row td{background:#FFF7ED;}
.premium-table tr.critical-row td{background:#FEF2F2; font-weight:800;}
.backlog-alert{background:linear-gradient(135deg,#7F1D1D 0%,#DC2626 100%);color:#FFFFFF;border-radius:18px;padding:16px 18px;margin:12px 0 16px 0;box-shadow:0 10px 24px rgba(185,28,28,.18);border:1px solid rgba(255,255,255,.18);}
.backlog-alert-title{font-size:.80rem;text-transform:uppercase;letter-spacing:.08em;font-weight:900;opacity:.82;}
.backlog-alert-value{font-size:1.28rem;font-weight:950;margin-top:5px;line-height:1.18;}
.backlog-alert-sub{font-size:.82rem;opacity:.88;margin-top:5px;}
.premium-table tr.attention-row td{background:#FFF7ED;}
.premium-table tr.critical-row td{background:#FEE2E2; font-weight:850;}
.engineer-table td:nth-child(1), .engineer-table th:nth-child(1){text-align:left;}
.engineer-table td:nth-child(7), .engineer-table th:nth-child(7), .engineer-table td:nth-child(8), .engineer-table th:nth-child(8){text-align:left;}
.premium-table td.total-col{font-weight:900; color:var(--interey-blue-2); background:#EEF3F8;}
.status-good{color:#047857; font-weight:900;}
.status-warn{color:#B45309; font-weight:900;}
.status-bad{color:#B91C1C; font-weight:900;}
.table-caption-premium{font-size:.78rem; color:#64748B; margin-top:-8px; margin-bottom:8px;}

@media (max-width: 1100px){
    .radar-grid{grid-template-columns: repeat(2, minmax(0, 1fr));}
    .hero-date{text-align:left;}
}


/* NEXT LEVEL v56 */
.exec-pulse-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin:4px 0 18px 0;}
.exec-pulse{background:#FFFFFF;border:1px solid rgba(18,62,112,.12);border-radius:16px;padding:12px 14px;box-shadow:0 7px 18px rgba(15,23,42,.045);position:relative;overflow:hidden;}
.exec-pulse:before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px;background:var(--interey-blue);}
.exec-pulse.green:before{background:var(--interey-green);}.exec-pulse.red:before{background:var(--interey-red);}.exec-pulse.yellow:before{background:var(--interey-yellow);}.exec-pulse.gray:before{background:var(--interey-gray);}
.exec-pulse-label{font-size:.70rem;text-transform:uppercase;letter-spacing:.075em;color:#64748B;font-weight:900;}
.exec-pulse-value{font-size:1.18rem;color:#0B1F4D;font-weight:950;margin-top:5px;line-height:1.08;}
.exec-pulse-sub{font-size:.76rem;color:#64748B;margin-top:5px;line-height:1.28;}
.drill-wrap{background:linear-gradient(135deg,#F8FAFC 0%,#FFFFFF 100%);border:1px solid rgba(18,62,112,.14);border-radius:20px;padding:15px 16px;margin:10px 0 18px 0;box-shadow:0 8px 22px rgba(15,23,42,.05);}
.drill-head{display:flex;justify-content:space-between;gap:12px;align-items:center;margin-bottom:12px;}
.drill-title{font-size:1.02rem;font-weight:950;color:#0B1F4D;}.drill-sub{font-size:.77rem;color:#64748B;}
.drill-badge{background:#EAF2FB;border:1px solid rgba(18,62,112,.16);color:#123E70;border-radius:999px;padding:6px 10px;font-size:.73rem;font-weight:900;white-space:nowrap;}
.drill-grid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:9px;}
.drill-tile{background:#FFFFFF;border:1px solid #E2E8F0;border-radius:14px;padding:10px 11px;}
.drill-label{font-size:.68rem;text-transform:uppercase;letter-spacing:.05em;color:#64748B;font-weight:850;}
.drill-value{font-size:1.02rem;color:#0B1F4D;font-weight:950;margin-top:4px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.drill-note{font-size:.72rem;color:#64748B;margin-top:4px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
@media (max-width:1200px){.exec-pulse-grid{grid-template-columns:repeat(2,minmax(0,1fr));}.drill-grid{grid-template-columns:repeat(2,minmax(0,1fr));}}
@media (max-width:760px){.exec-pulse-grid,.drill-grid{grid-template-columns:1fr;}.drill-head{display:block;}.drill-badge{display:inline-block;margin-top:8px;}}

/* V70 · Premium charts & compact alerts */
.closing-alert{
    background:linear-gradient(135deg,#FFF7E8 0%,#FFFBEF 100%);
    border:1px solid rgba(217,119,6,.18);
    border-left:4px solid #D97706;
    border-radius:14px;
    padding:12px 14px;
    margin:0 0 14px 0;
    box-shadow:0 6px 18px rgba(15,23,42,.04);
}
.closing-alert-title{
    font-size:.72rem;
    color:#A65E00;
    text-transform:uppercase;
    font-weight:900;
    letter-spacing:.08em;
}
.closing-alert-body{
    margin-top:4px;
    color:#7C5B18;
    font-size:.83rem;
    line-height:1.35;
}
.closing-alert-body b{color:#8A4B08;}

.bullet-card{
    background:linear-gradient(135deg,#FFFFFF 0%,#F8FAFD 100%);
    border:1px solid rgba(18,62,112,.12);
    border-radius:18px;
    padding:16px 18px 14px 18px;
    box-shadow:0 8px 22px rgba(15,23,42,.05);
    margin:6px 0 16px 0;
}
.bullet-card-head{
    display:flex;
    justify-content:space-between;
    gap:12px;
    align-items:flex-start;
    margin-bottom:10px;
}
.bullet-title{
    color:#0B1F4D;
    font-size:1.02rem;
    font-weight:950;
    line-height:1.2;
}
.bullet-sub{
    color:#64748B;
    font-size:.76rem;
    margin-top:4px;
}
.bullet-value-block{
    text-align:right;
}
.bullet-value{
    color:#0B1F4D;
    font-size:2.05rem;
    font-weight:950;
    line-height:1;
}
.bullet-status{
    display:inline-block;
    margin-top:5px;
    border-radius:999px;
    padding:5px 9px;
    font-size:.68rem;
    font-weight:900;
    border:1px solid #E2E8F0;
    background:#F8FAFC;
    color:#526174;
}
.bullet-status.good{background:#EAF7F4;color:#0F766E;border-color:#BEE3DB;}
.bullet-status.warn{background:#FFF7E6;color:#A65E00;border-color:#F4D39A;}
.bullet-status.bad{background:#FDECEC;color:#B42318;border-color:#F3C0C0;}
.bullet-track{
    position:relative;
    height:18px;
    border-radius:999px;
    overflow:hidden;
    background:#E9EEF5;
    box-shadow:inset 0 1px 2px rgba(15,23,42,.06);
}
.bullet-zone-red{
    position:absolute;left:0;top:0;bottom:0;width:60%;
    background:linear-gradient(90deg,#FCE1E1 0%,#F8D8D8 100%);
}
.bullet-zone-amber{
    position:absolute;left:60%;top:0;bottom:0;width:6.6667%;
    background:linear-gradient(90deg,#F9E9B8 0%,#F2DE97 100%);
}
.bullet-zone-green{
    position:absolute;left:66.6667%;top:0;bottom:0;width:33.3333%;
    background:linear-gradient(90deg,#D9F2E5 0%,#C7E9D5 100%);
}
.bullet-progress{
    position:absolute;left:0;top:0;bottom:0;
    background:linear-gradient(90deg,#163C74 0%,#0B1F4D 100%);
    opacity:.96;
}
.bullet-marker{
    position:absolute;top:-4px;bottom:-4px;width:3px;background:#0B1F4D;border-radius:999px;
    box-shadow:0 0 0 3px rgba(255,255,255,.88), 0 2px 8px rgba(11,31,77,.18);
}
.bullet-scale{
    display:flex;justify-content:space-between;gap:10px;
    color:#64748B;font-size:.67rem;margin-top:6px;
}
.bullet-kpis{
    display:grid;
    grid-template-columns:repeat(3,minmax(0,1fr));
    gap:10px;
    margin-top:12px;
}
.bullet-mini{
    border:1px solid #E7EDF4;
    border-radius:14px;
    padding:10px 12px;
    background:#FFFFFF;
}
.bullet-mini-label{
    color:#64748B;
    font-size:.67rem;
    text-transform:uppercase;
    letter-spacing:.06em;
    font-weight:900;
}
.bullet-mini-value{
    color:#0B1F4D;
    font-size:1.02rem;
    font-weight:950;
    margin-top:5px;
}
.bullet-mini-sub{
    color:#718096;
    font-size:.71rem;
    margin-top:4px;
}
@media (max-width:900px){
    .bullet-card-head{display:block;}
    .bullet-value-block{text-align:left;margin-top:8px;}
    .bullet-kpis{grid-template-columns:1fr;}
}

.chart-caption-premium{
    color:#64748B;
    font-size:.76rem;
    margin-top:-2px;
    margin-bottom:8px;
}


/* V73 · Dirección compacta & gobierno de datos */
.data-status-strip{
    display:grid;
    grid-template-columns:1.25fr repeat(3,minmax(0,.85fr));
    background:#FFFFFF;
    border:1px solid #DDE5EE;
    border-radius:14px;
    overflow:hidden;
    margin:4px 0 14px 0;
    box-shadow:0 5px 16px rgba(15,23,42,.04);
}
.data-status-main,.data-status-cell{padding:10px 13px;}
.data-status-main{background:#F8FAFC;}
.data-status-cell{border-left:1px solid #E7EDF4;}
.data-status-label{color:#64748B;font-size:.63rem;font-weight:900;text-transform:uppercase;letter-spacing:.07em;}
.data-status-value{color:#0B1F4D;font-size:.84rem;font-weight:900;margin-top:3px;}
.data-status-value.good{color:#0F766E;}
.data-status-value.warn{color:#A65E00;}

.backlog-cover-strip{
    display:grid;
    grid-template-columns:1.2fr repeat(4,minmax(0,.85fr));
    align-items:stretch;
    background:#FFFFFF;
    border:1px solid #DDE5EE;
    border-radius:16px;
    overflow:hidden;
    margin:10px 0 16px 0;
    box-shadow:0 6px 18px rgba(15,23,42,.045);
}
.backlog-cover-main,.backlog-cover-cell{padding:12px 14px;}
.backlog-cover-main{background:linear-gradient(135deg,#F7FAFD 0%,#FFFFFF 100%);}
.backlog-cover-cell{border-left:1px solid #E7EDF4;}
.backlog-cover-kicker{color:#64748B;font-size:.64rem;font-weight:900;text-transform:uppercase;letter-spacing:.07em;}
.backlog-cover-title{color:#0B1F4D;font-size:.90rem;font-weight:950;margin-top:4px;}
.backlog-cover-sub{color:#718096;font-size:.69rem;margin-top:4px;}
.backlog-cover-value{color:#0B1F4D;font-size:1.05rem;font-weight:950;margin-top:4px;}
.backlog-cover-value.good{color:#0F766E;}
.backlog-cover-value.warn{color:#A65E00;}
.backlog-cover-value.bad{color:#B42318;}

@media(max-width:1000px){
    .data-status-strip{grid-template-columns:1fr 1fr;}
    .data-status-main{grid-column:1/-1;border-bottom:1px solid #E7EDF4;}
    .backlog-cover-strip{grid-template-columns:1fr 1fr;}
    .backlog-cover-main{grid-column:1/-1;border-bottom:1px solid #E7EDF4;}
}
@media(max-width:640px){
    .data-status-strip,.backlog-cover-strip{grid-template-columns:1fr;}
    .data-status-main,.backlog-cover-main{grid-column:auto;}
    .data-status-cell,.backlog-cover-cell{border-left:none;border-top:1px solid #E7EDF4;}
}


/* V76 · Planeación 2027 */
.plan27-hero{
    background:linear-gradient(135deg,#0B1F4D 0%,#123E70 72%,#1C568D 100%);
    color:#FFFFFF;
    border-radius:20px;
    padding:16px 18px;
    margin:8px 0 14px 0;
    box-shadow:0 10px 28px rgba(11,31,77,.14);
}
.plan27-kicker{
    font-size:.67rem;
    font-weight:900;
    letter-spacing:.11em;
    text-transform:uppercase;
    color:rgba(255,255,255,.68);
}
.plan27-title{
    font-size:1.30rem;
    font-weight:950;
    letter-spacing:-.025em;
    margin-top:4px;
}
.plan27-sub{
    font-size:.80rem;
    color:rgba(255,255,255,.78);
    margin-top:5px;
    line-height:1.35;
}
.plan27-grid{
    display:grid;
    grid-template-columns:repeat(4,minmax(0,1fr));
    gap:10px;
    margin:10px 0 14px 0;
}
.plan27-card{
    background:#FFFFFF;
    border:1px solid #DDE5EE;
    border-top:4px solid #123E70;
    border-radius:16px;
    padding:13px 14px;
    box-shadow:0 6px 18px rgba(15,23,42,.05);
    min-height:112px;
}
.plan27-card.good{border-top-color:#118C7E;}
.plan27-card.warn{border-top-color:#D97706;}
.plan27-card.bad{border-top-color:#D52B24;}
.plan27-card.gray{border-top-color:#64748B;}
.plan27-label{
    color:#64748B;
    font-size:.66rem;
    font-weight:900;
    text-transform:uppercase;
    letter-spacing:.065em;
}
.plan27-value{
    color:#0B1F4D;
    font-size:1.36rem;
    font-weight:950;
    letter-spacing:-.035em;
    margin-top:7px;
}
.plan27-card.good .plan27-value{color:#0F766E;}
.plan27-card.warn .plan27-value{color:#A65E00;}
.plan27-card.bad .plan27-value{color:#B42318;}
.plan27-subvalue{
    color:#718096;
    font-size:.72rem;
    margin-top:5px;
    line-height:1.28;
}
.plan27-command{
    display:grid;
    grid-template-columns:1.25fr repeat(3,minmax(0,.8fr));
    background:#FFFFFF;
    border:1px solid #DDE5EE;
    border-radius:17px;
    overflow:hidden;
    margin:10px 0 14px 0;
    box-shadow:0 6px 18px rgba(15,23,42,.045);
}
.plan27-command-main,.plan27-command-cell{padding:12px 14px;}
.plan27-command-main{background:#F8FAFC;}
.plan27-command-cell{border-left:1px solid #E7EDF4;}
.plan27-command-label{
    color:#64748B;
    font-size:.64rem;
    font-weight:900;
    text-transform:uppercase;
    letter-spacing:.07em;
}
.plan27-command-value{
    color:#0B1F4D;
    font-size:1.02rem;
    font-weight:950;
    margin-top:5px;
}
.plan27-command-text{
    color:#64748B;
    font-size:.71rem;
    line-height:1.30;
    margin-top:4px;
}
.plan27-status{
    display:inline-block;
    border-radius:999px;
    padding:5px 9px;
    margin-top:6px;
    font-size:.68rem;
    font-weight:900;
    background:#F1F5F9;
    color:#526174;
}
.plan27-status.good{background:#EAF7F4;color:#0F766E;}
.plan27-status.warn{background:#FFF7E6;color:#A65E00;}
.plan27-status.bad{background:#FDECEC;color:#B42318;}
.plan27-note{
    background:#F7F9FC;
    border-left:4px solid #123E70;
    border-radius:12px;
    padding:10px 12px;
    color:#475569;
    font-size:.76rem;
    line-height:1.35;
    margin:8px 0 14px 0;
}
@media(max-width:1050px){
    .plan27-grid{grid-template-columns:repeat(2,minmax(0,1fr));}
    .plan27-command{grid-template-columns:1fr 1fr;}
    .plan27-command-main{grid-column:1/-1;border-bottom:1px solid #E7EDF4;}
}
@media(max-width:640px){
    .plan27-grid,.plan27-command{grid-template-columns:1fr;}
    .plan27-command-main{grid-column:auto;}
    .plan27-command-cell{border-left:none;border-top:1px solid #E7EDF4;}
}

""", unsafe_allow_html=True)

MONTHS_ES = {1:"Ene",2:"Feb",3:"Mar",4:"Abr",5:"May",6:"Jun",7:"Jul",8:"Ago",9:"Sep",10:"Oct",11:"Nov",12:"Dic"}
MONTH_ORDER = [MONTHS_ES[i] for i in range(1,13)]
MONTHS_FULL_TO_NUM = {"ENERO":1,"FEBRERO":2,"MARZO":3,"ABRIL":4,"MAYO":5,"JUNIO":6,"JULIO":7,"AGOSTO":8,"SEPTIEMBRE":9,"SETIEMBRE":9,"OCTUBRE":10,"NOVIEMBRE":11,"DICIEMBRE":12}
START_DATE = pd.Timestamp("2024-01-01")
VALID_YEARS = [2024, 2025, 2026]
PROJECT_TARGETS = {2024: 500000, 2025: 700000, 2026: 750000}
STORE_TARGETS = {2024: 150000, 2025: 250000, 2026: 275000}
ACTIVE_PROJECT_ENGINEERS_FOR_TARGET = 4
EXCLUDE_FROM_ENGINEER_ANALYSIS = {"ORLANDO MARTINEZ", "ANA MARGARITA SAHAGUN"}

DEFAULT_PROJECT_FILES = ["Proyectos 2024-2026.csv", "Reporte 2024-2026.csv", "Reporte 2024-2026.csv"]
DEFAULT_STORE_FILES = ["Tienda 2024-2026.csv", "reporte 2024-2026.csv"]
DEFAULT_EXPENSE_FILES = ["GASTOS OPERATIVOS 2026.xlsx", "GASTOS OPERATIVOS 2026(8).xlsx", "VENTAS INTEREY PROYECTOS Y TIENDA 2026.xlsx", "Gastos INTEREY 2026.xlsx", "Gastos 2026.xlsx"]
DEFAULT_BACKLOG_FILES = ["Proyectos en ejecucion.csv", "Proyectos%20en%20ejecucion.csv", "Proyectos en ejecución.csv"]


def fmt_money(x):
    try:
        if pd.isna(x):
            return "$0"
        return f"${float(x):,.0f}"
    except Exception:
        return "$0"


def fmt_pct(x):
    try:
        if pd.isna(x):
            return "0.0%"
        return f"{float(x):,.1f}%"
    except Exception:
        return "0.0%"


def parse_money(x):
    if pd.isna(x):
        return pd.NA
    s = str(x).strip()
    if s == "" or s.lower() in ["nan", "none"]:
        return pd.NA
    # formato tipo ($ -494.61), (-6,484.63 %), $17.32
    neg = "(" in s and ")" in s
    s = s.replace("$", "").replace(",", "").replace("%", "").replace("(", "").replace(")", "").strip()
    s = s.replace(" ", "")
    try:
        val = float(s)
        return -abs(val) if neg else val
    except Exception:
        return pd.NA


def parse_date_project(series):
    dt = pd.to_datetime(series, format="%d/%m/%Y", errors="coerce")
    if dt.isna().all():
        dt = pd.to_datetime(series, dayfirst=True, errors="coerce")
    return dt


def parse_date_store(series):
    # Puede venir como "09:21 04/01/2024" o "04/01/2024"
    raw = series.astype(str).str.strip()
    extracted = raw.str.extract(r"(\d{1,2}/\d{1,2}/\d{4})", expand=False)
    candidate = extracted.fillna(raw)
    return pd.to_datetime(candidate, dayfirst=True, errors="coerce")


def add_time_cols(df):
    df["Año"] = df["Fecha"].dt.year
    df["Mes_Num"] = df["Fecha"].dt.month
    df["Mes"] = df["Mes_Num"].map(MONTHS_ES)
    df["Periodo"] = df["Fecha"].dt.strftime("%Y-%m")
    return df


def find_default_file(names):
    here = Path(__file__).resolve().parent

    # 1) Primero busca coincidencia exacta.
    for name in names:
        p = here / name
        if p.exists():
            return p

    # 2) Respaldo tolerante: permite variantes del nombre generadas al descargar/copiar archivos.
    patterns = []
    for name in names:
        stem = Path(name).stem
        suffix = Path(name).suffix
        if stem:
            patterns.append(f"{stem}*{suffix}")

    # Caso especial del archivo administrativo mensual de gastos.
    if any("GASTOS OPERATIVOS 2026" in str(n).upper() for n in names):
        patterns.insert(0, "GASTOS OPERATIVOS 2026*.xlsx")

    for pattern in patterns:
        matches = sorted(here.glob(pattern))
        if matches:
            return matches[0]

    return None


def load_projects(uploaded_file):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        p = find_default_file(DEFAULT_PROJECT_FILES)
        if p is None:
            return pd.DataFrame()
        df = pd.read_csv(p)

    for col in ["Promotor", "Cliente", "Moneda", "Descripcion"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    for col in ["TC", "Cotizado cliente", "Utilidad bruta", "Utilidad", "Utilidad después de indirectos"]:
        if col in df.columns:
            df[col] = df[col].apply(parse_money)

    if "Fecha" not in df.columns:
        return pd.DataFrame()
    df["Fecha"] = parse_date_project(df["Fecha"])
    df = add_time_cols(df)

    # Corte automático: conserva toda la información disponible desde 2024.
    df = df[(df["Fecha"] >= START_DATE) & (df["Año"].isin(VALID_YEARS))].copy()

    # Nota: Ana Margarita Sahagun y Orlando Martinez SÍ se incluyen en KPIs corporativos.
    # Solo se excluyen en los comparativos de desempeño por ingeniero/promotor.

    df["Moneda"] = df.get("Moneda", "MXN")
    df["Moneda"] = df["Moneda"].fillna("MXN").astype(str).str.upper()
    df["TC"] = df.get("TC", 1.0)
    df["TC"] = pd.to_numeric(df["TC"], errors="coerce").fillna(1.0)
    df["Tipo_Cambio_Aplicado"] = df.apply(lambda r: r["TC"] if r["Moneda"] == "USD" else 1.0, axis=1)

    df["Ventas_MXN"] = pd.to_numeric(df.get("Cotizado cliente", 0), errors="coerce").fillna(0) * df["Tipo_Cambio_Aplicado"]
    if "Utilidad bruta" not in df.columns:
        st.warning("El archivo de proyectos no trae la columna 'Utilidad bruta'. Se usará 'Utilidad después de indirectos' como respaldo.")
        util_source = "Utilidad después de indirectos" if "Utilidad después de indirectos" in df.columns else "Utilidad"
    else:
        util_source = "Utilidad bruta"
    df["Utilidad_Bruta_MXN"] = pd.to_numeric(df.get(util_source, 0), errors="coerce").fillna(0) * df["Tipo_Cambio_Aplicado"]
    df["Margen_Bruto_Pct"] = (df["Utilidad_Bruta_MXN"] / df["Ventas_MXN"].replace(0, pd.NA)) * 100
    df["Unidad"] = "Proyectos"
    return df


def load_backlog(uploaded_file):
    """Carga el snapshot vigente de proyectos con OC pendientes de facturar.

    Este archivo sustituye al anterior en cada corte mensual; no se acumula.
    """
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
        except Exception as exc:
            st.warning(f"No fue posible leer el archivo de ingresos comprometidos: {exc}")
            return pd.DataFrame()
    else:
        p = find_default_file(DEFAULT_BACKLOG_FILES)
        if p is None:
            return pd.DataFrame()
        try:
            df = pd.read_csv(p)
        except Exception as exc:
            st.warning(f"No fue posible leer el archivo base de ingresos comprometidos: {exc}")
            return pd.DataFrame()

    if df.empty:
        return pd.DataFrame()

    df.columns = [str(c).strip() for c in df.columns]
    required = ["Fecha", "Cliente", "Cotizado cliente"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        st.warning("El archivo de ingresos comprometidos no contiene: " + ", ".join(missing))
        return pd.DataFrame()

    for col in ["Promotor", "Cliente", "Descripcion", "Moneda", "Status"]:
        if col in df.columns:
            df[col] = df[col].fillna("").astype(str).str.strip()

    raw = df["Fecha"].astype(str).str.strip()
    dt = pd.to_datetime(raw, format="%d/%m/%y", errors="coerce")
    missing_dt = dt.isna()
    if missing_dt.any():
        dt.loc[missing_dt] = pd.to_datetime(raw.loc[missing_dt], format="%d/%m/%Y", errors="coerce")
    missing_dt = dt.isna()
    if missing_dt.any():
        dt.loc[missing_dt] = pd.to_datetime(raw.loc[missing_dt], dayfirst=True, errors="coerce")
    df["Fecha_OC"] = dt
    df = df[df["Fecha_OC"].notna()].copy()

    for col in ["TC", "Cotizado cliente"]:
        if col in df.columns:
            df[col] = df[col].apply(parse_money)

    df["Moneda"] = df.get("Moneda", "MXN")
    df["Moneda"] = df["Moneda"].fillna("MXN").astype(str).str.upper()
    df["TC"] = pd.to_numeric(df.get("TC", 1.0), errors="coerce").fillna(1.0)
    df["Tipo_Cambio_Aplicado"] = df.apply(lambda r: r["TC"] if r["Moneda"] == "USD" else 1.0, axis=1)
    df["Importe_Pendiente_MXN"] = pd.to_numeric(df["Cotizado cliente"], errors="coerce").fillna(0) * df["Tipo_Cambio_Aplicado"]

    today = pd.Timestamp.today().normalize()
    df["Dias_Abiertos"] = (today - df["Fecha_OC"].dt.normalize()).dt.days.clip(lower=0)
    df["Periodo_OC"] = df["Fecha_OC"].dt.to_period("M").astype(str)
    df["Mes_OC"] = df["Fecha_OC"].dt.month.map(MONTHS_ES)
    df["Proyecto"] = df.get("Descripcion", "Sin descripción")
    df["Responsable"] = df.get("Promotor", "Sin responsable")
    # El campo Id del archivo corresponde al número de proyecto.
    if "Id" in df.columns:
        df["Numero_Proyecto"] = pd.to_numeric(df["Id"], errors="coerce").astype("Int64")
    else:
        df["Numero_Proyecto"] = pd.Series([pd.NA] * len(df), dtype="Int64")

    def age_bucket(days):
        if days <= 30:
            return "🟢 0–30 días"
        if days <= 60:
            return "🟡 31–60 días"
        if days <= 90:
            return "🟠 61–90 días"
        return "🔴 Más de 90 días"

    df["Antigüedad"] = df["Dias_Abiertos"].apply(age_bucket)
    if "Id" in df.columns:
        df = df.drop_duplicates(subset=["Id"], keep="last")
    else:
        df = df.drop_duplicates(keep="last")
    return df.reset_index(drop=True)


def load_store(uploaded_file):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        p = find_default_file(DEFAULT_STORE_FILES)
        if p is None:
            return pd.DataFrame()
        df = pd.read_csv(p)

    for col in ["Cliente", "Status", "Pago", "Facturado"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    for col in ["SubTotal", "Total", "Util $", "Tienda $", "Desc $", "Iva $"]:
        if col in df.columns:
            df[col] = df[col].apply(parse_money)

    if "Fecha" not in df.columns:
        return pd.DataFrame()
    df["Fecha"] = parse_date_store(df["Fecha"])
    df = add_time_cols(df)
    df = df[(df["Fecha"] >= START_DATE) & (df["Año"].isin(VALID_YEARS))].copy()

    # TIENDA: solo considerar ventas activas.
    # Regla de negocio: cualquier registro con Status/Estatus cancelado NO debe afectar ventas, utilidad, forecast ni consolidado.
    if "Status" in df.columns:
        df["Status_Normalizado"] = df["Status"].fillna("").astype(str).str.strip().str.upper()
        df = df[df["Status_Normalizado"].eq("ACTIVO")].copy()

    df["Ventas_MXN"] = pd.to_numeric(df.get("Total", 0), errors="coerce").fillna(0)
    df["Utilidad_Bruta_MXN"] = pd.to_numeric(df.get("Util $", 0), errors="coerce").fillna(0)
    df["Margen_Bruto_Pct"] = (df["Utilidad_Bruta_MXN"] / df["Ventas_MXN"].replace(0, pd.NA)) * 100
    df["Promotor"] = "JAVIER VILLANUEVA"
    df["Unidad"] = "Tienda"
    return df


def load_expenses(expense_file):
    """
    Lee automáticamente GASTOS OPERATIVOS 2026.xlsx.

    Fuente oficial:
    - Proyectos: hoja RESUMEN, fila "Total general".
    - Tienda: hoja "GASTOS TIENDA 2026", bloque 2026,
      fila "GASTOS Total general".

    Los meses todavía no capturados permanecen como pendientes (NA),
    para no tratarlos como gasto $0.
    """
    empty_cols = [
        "Año", "Mes_Num", "Mes",
        "Gasto_Proyectos", "Gasto_Tienda",
        "Disponible_Proyectos", "Disponible_Tienda"
    ]

    try:
        if expense_file is not None:
            xls = pd.ExcelFile(expense_file)
        else:
            p = find_default_file(DEFAULT_EXPENSE_FILES)
            if p is None:
                st.warning(
                    "No encontré el archivo de gastos en GitHub/carpeta del dashboard. "
                    "Verifica que exista 'GASTOS OPERATIVOS 2026.xlsx'."
                )
                return pd.DataFrame(columns=empty_cols)
            xls = pd.ExcelFile(p)
    except Exception as exc:
        st.warning(f"No fue posible abrir el archivo de gastos: {exc}")
        return pd.DataFrame(columns=empty_cols)

    month_names = [
        "ENERO","FEBRERO","MARZO","ABRIL","MAYO","JUNIO",
        "JULIO","AGOSTO","SEPTIEMBRE","OCTUBRE","NOVIEMBRE","DICIEMBRE"
    ]

    # ---------- PROYECTOS ----------
    project_by_month = {m: pd.NA for m in range(1, 13)}
    project_available = {m: False for m in range(1, 13)}

    resumen_sheet = next(
        (s for s in xls.sheet_names if str(s).strip().upper() == "RESUMEN"),
        None
    )

    if resumen_sheet is None:
        st.warning("No encontré la hoja 'RESUMEN' en el archivo de gastos.")
    else:
        raw = pd.read_excel(xls, sheet_name=resumen_sheet, header=None)

        header_idx = next(
            (
                i for i in range(len(raw))
                if str(raw.iloc[i, 0]).strip().upper() == "CONCEPTO"
                and "ENERO" in [str(v).strip().upper() for v in raw.iloc[i].tolist()]
            ),
            None
        )

        total_idx = None
        if header_idx is not None:
            total_idx = next(
                (
                    i for i in range(header_idx + 1, len(raw))
                    if str(raw.iloc[i, 0]).strip().upper() == "TOTAL GENERAL"
                ),
                None
            )

        if header_idx is None or total_idx is None:
            st.warning("No pude identificar 'CONCEPTO' / 'Total general' en la hoja RESUMEN.")
        else:
            headers = [str(v).strip().upper() for v in raw.iloc[header_idx].tolist()]

            # Para Proyectos, las hojas mensuales existentes indican qué meses ya están capturados/cerrados.
            available_month_sheets = {
                str(s).strip().upper()
                for s in xls.sheet_names
                if str(s).strip().upper() in month_names
            }

            for m, month_name in enumerate(month_names, start=1):
                if month_name not in headers:
                    continue
                col_idx = headers.index(month_name)
                val = parse_money(raw.iloc[total_idx, col_idx])

                if month_name in available_month_sheets and not pd.isna(val):
                    project_by_month[m] = float(val)
                    project_available[m] = True

    # ---------- TIENDA ----------
    store_by_month = {m: pd.NA for m in range(1, 13)}
    store_available = {m: False for m in range(1, 13)}

    store_sheet = next(
        (s for s in xls.sheet_names if str(s).strip().upper() == "GASTOS TIENDA 2026"),
        None
    )
    if store_sheet is None:
        store_sheet = next(
            (s for s in xls.sheet_names if "GASTOS TIENDA" in str(s).upper()),
            None
        )

    if store_sheet is None:
        st.warning("No encontré la hoja 'GASTOS TIENDA 2026'.")
    else:
        raw_store = pd.read_excel(xls, sheet_name=store_sheet, header=None)

        # Localiza primero el bloque 2026 para no leer por accidente el bloque 2025.
        block_start = next(
            (
                i for i in range(len(raw_store))
                if "GASTOS INTEREY STORE" in str(raw_store.iloc[i, 0]).strip().upper()
                and "2026" in str(raw_store.iloc[i, 0]).strip().upper()
            ),
            None
        )

        header_idx = None
        total_idx = None

        if block_start is not None:
            header_idx = next(
                (
                    i for i in range(block_start + 1, len(raw_store))
                    if str(raw_store.iloc[i, 0]).strip().upper() == "CONCEPTO"
                ),
                None
            )

        if header_idx is not None:
            total_idx = next(
                (
                    i for i in range(header_idx + 1, len(raw_store))
                    if str(raw_store.iloc[i, 0]).strip().upper() == "GASTOS TOTAL GENERAL"
                ),
                None
            )

        if header_idx is None or total_idx is None:
            st.warning(
                "No pude identificar el bloque 2026 / 'GASTOS Total general' "
                "en la hoja GASTOS TIENDA 2026."
            )
        else:
            headers = [str(v).strip().upper() for v in raw_store.iloc[header_idx].tolist()]
            detail = raw_store.iloc[header_idx + 1:total_idx].copy()

            # Detecta el último mes realmente capturado en el bloque 2026.
            last_available_month = 0
            for m, month_name in enumerate(month_names, start=1):
                if month_name not in headers:
                    continue
                col_idx = headers.index(month_name)
                month_detail = detail.iloc[:, col_idx]

                # Si hay al menos una partida informada en ese mes, el mes está disponible.
                if month_detail.notna().any():
                    last_available_month = m

            for m, month_name in enumerate(month_names, start=1):
                if month_name not in headers or m > last_available_month:
                    continue

                col_idx = headers.index(month_name)
                val = parse_money(raw_store.iloc[total_idx, col_idx])
                if not pd.isna(val):
                    store_by_month[m] = float(val)
                    store_available[m] = True

    rows = []
    for m in range(1, 13):
        rows.append({
            "Año": 2026,
            "Mes_Num": m,
            "Mes": MONTHS_ES[m],
            "Gasto_Proyectos": project_by_month[m],
            "Gasto_Tienda": store_by_month[m],
            "Disponible_Proyectos": project_available[m],
            "Disponible_Tienda": store_available[m],
        })

    result = pd.DataFrame(rows)

    # Validación administrativa visible: estos valores deben conciliar con el Excel.
    p_total = pd.to_numeric(
        result.loc[result["Disponible_Proyectos"], "Gasto_Proyectos"],
        errors="coerce"
    ).sum()
    t_total = pd.to_numeric(
        result.loc[result["Disponible_Tienda"], "Gasto_Tienda"],
        errors="coerce"
    ).sum()

    st.sidebar.caption(f"Excel gastos Proyectos reconocido: {fmt_money(p_total)}")
    st.sidebar.caption(f"Excel gastos Tienda reconocido: {fmt_money(t_total)}")

    return result


def expenses_dict(expenses_df, year, months, unidad):
    col = "Gasto_Proyectos" if unidad == "Proyectos" else "Gasto_Tienda"
    if expenses_df.empty or col not in expenses_df.columns:
        return {m: 0.0 for m in months}
    temp = expenses_df[(expenses_df["Año"] == year) & (expenses_df["Mes_Num"].isin(months))].copy()
    temp[col] = pd.to_numeric(temp[col], errors="coerce")
    by_month = temp.groupby("Mes_Num")[col].sum(min_count=1).to_dict()
    return {m: float(by_month[m]) if m in by_month and pd.notna(by_month[m]) else 0.0 for m in months}


def expense_missing_months(expenses_df, year, months, unidad):
    flag_col = "Disponible_Proyectos" if unidad == "Proyectos" else "Disponible_Tienda"
    if expenses_df.empty or flag_col not in expenses_df.columns:
        return list(months)
    temp = expenses_df[expenses_df["Año"] == year].set_index("Mes_Num")
    missing = []
    for m in months:
        if m not in temp.index or not bool(temp.loc[m, flag_col]):
            missing.append(m)
    return missing

def closed_months_for_year(df, year):
    months = sorted(df.loc[df["Año"] == year, "Mes_Num"].dropna().astype(int).unique().tolist())
    if not months:
        return []
    # Regla: si el último mes cargado está incompleto por corte futuro, se excluye solo si supera corte real.
    # Para 2026 el corte es mayo, así que mayo sí es mes cerrado del análisis solicitado.
    return months


def ytd_months_for_selected_year(selected_year, projects_df=None, store_df=None):
    """Devuelve Enero..último mes con ventas del año seleccionado."""
    months = set()
    for df in [projects_df, store_df]:
        if df is not None and not df.empty and "Año" in df.columns and "Mes_Num" in df.columns:
            months.update(
                df.loc[df["Año"] == selected_year, "Mes_Num"]
                .dropna().astype(int).tolist()
            )
    if not months:
        return list(range(1, 13))
    return list(range(1, max(months) + 1))


def latest_data_date(*dfs):
    dates = []
    for df in dfs:
        if df is not None and not df.empty and "Fecha" in df.columns:
            d = pd.to_datetime(df["Fecha"], errors="coerce").max()
            if pd.notna(d):
                dates.append(d)
    return max(dates) if dates else None


def fmt_date_es(dt):
    if dt is None or pd.isna(dt):
        return "Sin fecha"
    full = {1:"Enero",2:"Febrero",3:"Marzo",4:"Abril",5:"Mayo",6:"Junio",
            7:"Julio",8:"Agosto",9:"Septiembre",10:"Octubre",11:"Noviembre",12:"Diciembre"}
    dt = pd.Timestamp(dt)
    return f"{dt.day:02d} {full[dt.month]} {dt.year}"

def yoy(curr, prev):
    if prev in [0, None] or pd.isna(prev):
        return None
    return ((curr - prev) / prev) * 100


def card(label, value, sub="", style=""):
    return f"""
    <div class="kpi-card {style}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>
    """


def trend_note(text):
    st.markdown(f'<div class="trend-note">{text}</div>', unsafe_allow_html=True)


def radar_interey(consol_fc, proj_fc, store_fc):
    """
    Radar INTEREY 4.0 · Executive Command Bar.
    Resume el estado corporativo en una sola lectura, cuatro señales y una acción prioritaria.
    """
    gap = float(consol_fc.get("gap", 0) or 0)
    cumplimiento = float(consol_fc.get("cumplimiento", 0) or 0)
    utilidad_neta_proy = float(consol_fc.get("utilidad_neta_proy", 0) or 0)
    venta_req = float(consol_fc.get("venta_req", 0) or 0)

    proj_cump = float(proj_fc.get("cumplimiento", 0) or 0)
    store_cump = float(store_fc.get("cumplimiento", 0) or 0)

    emoji, _, forecast_status = status_from_pct(cumplimiento)

    def radar_class_from_pct(value):
        if value >= 100:
            return "good", "En meta"
        if value >= 90:
            return "warn", "Seguimiento"
        return "bad", "Riesgo"

    proj_class, proj_status = radar_class_from_pct(proj_cump)
    store_class, store_status = radar_class_from_pct(store_cump)

    if utilidad_neta_proy > 0:
        util_class = "good"
        util_status = "Cierre positivo"
    elif utilidad_neta_proy == 0:
        util_class = "neutral"
        util_status = "Punto de equilibrio"
    else:
        util_class = "bad"
        util_status = "Cierre negativo"

    if gap >= 0:
        gap_class = "good"
        gap_label = "Excedente"
        gap_status = "Sobre meta"
    elif cumplimiento >= 90:
        gap_class = "warn"
        gap_label = "Brecha"
        gap_status = "Recuperable"
    else:
        gap_class = "bad"
        gap_label = "Brecha"
        gap_status = "Bajo objetivo"

    if cumplimiento >= 100:
        headline = "INTEREY proyecta cerrar por encima de la meta anual."
        headline_sub = "El ritmo comercial actual permite una lectura favorable; el foco pasa a proteger margen y ejecución."
    elif cumplimiento >= 90:
        headline = "INTEREY está cerca de la meta anual y requiere seguimiento."
        headline_sub = "El cierre depende de sostener el ritmo comercial y controlar gastos durante los meses restantes."
    else:
        headline = "INTEREY proyecta cerrar por debajo de la meta anual."
        headline_sub = "La prioridad es recuperar la brecha comercial sin comprometer la rentabilidad."

    if gap >= 0:
        action_label = "Prioridad ejecutiva"
        action_text = "Proteger el excedente proyectado y sostener la rentabilidad del cierre."
        action_value = fmt_money_signed(gap)
    else:
        action_label = "Acción prioritaria"
        action_text = "Venta promedio mensual requerida para llevar la proyección hacia la meta anual."
        action_value = fmt_money(venta_req)

    html = f"""
    <div class="radar-exec">
        <div class="radar-exec-top">
            <div class="radar-exec-brand">
                <div class="radar-exec-icon">📡</div>
                <div>
                    <div class="radar-exec-title">Radar INTEREY 4.0</div>
                    <div class="radar-exec-kicker">Executive Command Bar</div>
                </div>
            </div>
            <div class="radar-exec-status">{emoji} ESTADO GENERAL · {forecast_status.upper()}</div>
        </div>

        <div class="radar-exec-summary">
            <div class="radar-exec-summary-label">Lectura ejecutiva</div>
            <div class="radar-exec-summary-title">{headline}</div>
            <div class="radar-exec-summary-sub">{headline_sub}</div>
        </div>

        <div class="radar-exec-grid">
            <div class="radar-exec-metric {store_class}">
                <div class="radar-exec-label">
                    <span class="radar-exec-signal">
                        <span class="radar-exec-dot {store_class}"></span>Tienda
                    </span>
                </div>
                <div class="radar-exec-value">{fmt_pct(store_cump)}</div>
                <div class="radar-exec-meta">{store_status} · cumplimiento proyectado vs meta anual</div>
            </div>

            <div class="radar-exec-metric {proj_class}">
                <div class="radar-exec-label">
                    <span class="radar-exec-signal">
                        <span class="radar-exec-dot {proj_class}"></span>Proyectos
                    </span>
                </div>
                <div class="radar-exec-value">{fmt_pct(proj_cump)}</div>
                <div class="radar-exec-meta">{proj_status} · cumplimiento proyectado vs meta anual</div>
            </div>

            <div class="radar-exec-metric {util_class}">
                <div class="radar-exec-label">
                    <span class="radar-exec-signal">
                        <span class="radar-exec-dot {util_class}"></span>Utilidad estimada
                    </span>
                </div>
                <div class="radar-exec-value">{fmt_money_compact(utilidad_neta_proy)}</div>
                <div class="radar-exec-meta">{util_status} · utilidad neta proyectada al cierre</div>
            </div>

            <div class="radar-exec-metric {gap_class}">
                <div class="radar-exec-label">
                    <span class="radar-exec-signal">
                        <span class="radar-exec-dot {gap_class}"></span>{gap_label}
                    </span>
                </div>
                <div class="radar-exec-value">{fmt_money_compact(gap)}</div>
                <div class="radar-exec-meta">{gap_status} · diferencia proyectada contra meta anual</div>
            </div>
        </div>

        <div class="radar-exec-action">
            <div class="radar-exec-action-left">
                <div class="radar-exec-action-icon">🎯</div>
                <div>
                    <div class="radar-exec-action-label">{action_label}</div>
                    <div class="radar-exec-action-text">{action_text}</div>
                </div>
            </div>
            <div class="radar-exec-action-value">{action_value}</div>
        </div>
    </div>
    """
    # st.html renderiza HTML directamente y evita que Markdown interprete
    # la sangría interna como bloques de código.
    st.html(html)


def status_from_pct(pct, green=100, yellow=90):
    try:
        pct = float(pct)
    except Exception:
        return "🔴", "red", "Riesgo alto"
    if pct >= green:
        return "🟢", "green", "En línea"
    if pct >= yellow:
        return "🟡", "yellow", "Riesgo moderado"
    return "🔴", "red", "Riesgo alto"


def compliance_text(pct):
    emoji, _, status = status_from_pct(pct)
    return f"{emoji} Cumplimiento proyectado: {fmt_pct(pct)} · {status}"


def gap_label_and_style(gap):
    if gap >= 0:
        return "🟢 Excedente proyectado", "green", "proyección arriba de meta"
    return "🔴 Faltante proyectado", "red", "proyección debajo de meta"


def fmt_money_signed(x):
    try:
        x = float(x)
    except Exception:
        x = 0
    sign = "+" if x > 0 else ""
    return f"{sign}${x:,.0f}"


def fmt_money_compact(x):
    try:
        x = float(x)
    except Exception:
        x = 0
    sign = "-" if x < 0 else ""
    ax = abs(x)
    if ax >= 1_000_000:
        return f"{sign}${ax/1_000_000:,.2f} M"
    if ax >= 1_000:
        return f"{sign}${ax/1_000:,.0f} K"
    return f"{sign}${ax:,.0f}"


def summary_metrics(df):
    ventas = df["Ventas_MXN"].sum() if not df.empty else 0
    utilidad = df["Utilidad_Bruta_MXN"].sum() if not df.empty else 0
    margen = utilidad / ventas * 100 if ventas else 0
    clientes = df["Cliente"].nunique() if "Cliente" in df.columns and not df.empty else 0
    ticket = ventas / clientes if clientes else 0
    return ventas, utilidad, margen, clientes, ticket


def expense_inputs(prefix, year, months):
    st.sidebar.markdown(f"### Gastos {prefix} {year}")
    expenses = {}
    cols = st.sidebar.columns(2)
    for idx, m in enumerate(months):
        with cols[idx % 2]:
            expenses[m] = st.number_input(
                f"{prefix} {MONTHS_ES[m]}", min_value=0.0, value=0.0, step=10000.0, format="%.0f", key=f"gasto_{prefix}_{year}_{m}"
            )
    return expenses


def forecast_block(label, df_ytd, gastos_dict, meta_mensual, months_ytd, multiplier=1):
    meses_count = max(len(months_ytd), 1)
    ventas_ytd = df_ytd["Ventas_MXN"].sum() if not df_ytd.empty else 0
    util_ytd = df_ytd["Utilidad_Bruta_MXN"].sum() if not df_ytd.empty else 0
    gasto_ytd = sum(float(gastos_dict.get(m, 0)) for m in months_ytd)
    utilidad_neta_ytd = util_ytd - gasto_ytd
    margen_neto_ytd = utilidad_neta_ytd / ventas_ytd * 100 if ventas_ytd else 0

    promedio_ventas = ventas_ytd / meses_count
    promedio_util = util_ytd / meses_count
    promedio_gasto = gasto_ytd / meses_count if meses_count else 0

    forecast_ventas = promedio_ventas * 12
    forecast_util = promedio_util * 12
    gasto_anual_proy = promedio_gasto * 12
    utilidad_neta_proy = forecast_util - gasto_anual_proy
    margen_neto_proy = utilidad_neta_proy / forecast_ventas * 100 if forecast_ventas else 0

    meta_anual = meta_mensual * 12 * multiplier
    cumplimiento = forecast_ventas / meta_anual * 100 if meta_anual else 0
    gap = forecast_ventas - meta_anual
    meses_restantes = max(12 - meses_count, 0)
    venta_req = (meta_anual - ventas_ytd) / meses_restantes if meses_restantes else 0
    return {
        "label": label,
        "ventas_ytd": ventas_ytd,
        "utilidad_bruta_ytd": util_ytd,
        "gasto_ytd": gasto_ytd,
        "utilidad_neta_ytd": utilidad_neta_ytd,
        "margen_neto_ytd": margen_neto_ytd,
        "forecast_ventas": forecast_ventas,
        "forecast_utilidad_bruta": forecast_util,
        "gasto_anual_proy": gasto_anual_proy,
        "utilidad_neta_proy": utilidad_neta_proy,
        "margen_neto_proy": margen_neto_proy,
        "meta_anual": meta_anual,
        "cumplimiento": cumplimiento,
        "gap": gap,
        "venta_req": venta_req,
        "meses_restantes": meses_restantes,
    }


def style_exec_chart(fig, height=390, money_axis=False, legend=True):
    """Estilo gráfico ejecutivo INTEREY consistente y limpio."""
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=height,
        margin=dict(l=20, r=18, t=60, b=38),
        font=dict(color="#334155", family="Arial"),
        title=dict(font=dict(size=17, color="#0B1F4D"), x=0.01, xanchor="left"),
        hoverlabel=dict(bgcolor="#0B1F4D", font_color="#FFFFFF"),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.03, xanchor="right", x=1,
            title_text=""
        ) if legend else dict(visible=False),
    )
    fig.update_xaxes(showgrid=False, linecolor="#DCE3EC", tickfont=dict(color="#64748B"), title_text="")
    fig.update_yaxes(gridcolor="#E9EEF5", zeroline=False, tickfont=dict(color="#64748B"), title_text="")
    if money_axis:
        fig.update_yaxes(tickprefix="$", tickformat=",.0f")
    return fig


PLOT_CONFIG = {"displayModeBar": False, "responsive": True}


def _selected_plotly_point(event):
    """Extrae (año, mes) desde el estado real de selección de Streamlit/Plotly."""
    if event is None:
        return None

    try:
        # Streamlit 1.61 entrega PlotlyState, compatible con atributo y diccionario.
        selection = getattr(event, "selection", None)
        if selection is None and hasattr(event, "get"):
            selection = event.get("selection", {})

        points = getattr(selection, "points", None)
        if points is None and hasattr(selection, "get"):
            points = selection.get("points", [])

        if not points:
            return None

        point = points[0]
        if hasattr(point, "get"):
            custom = point.get("customdata")
            x = point.get("x")
            curve_number = point.get("curve_number")
        else:
            custom = getattr(point, "customdata", None)
            x = getattr(point, "x", None)
            curve_number = getattr(point, "curve_number", None)

        # Nuestra gráfica lleva customdata=[Año, Mes_Num].
        if custom is not None and len(custom) >= 2:
            return int(custom[0]), int(custom[1])

        # Respaldo: el eje X siempre es Mes_Num.
        if x is not None:
            return None, int(round(float(x)))

    except Exception:
        return None

    return None


@st.fragment
def render_month_chart_fragment(
    df, monthly, title, ycol, key, detail_label,
    interactive=True, target_map=None, show_explorer=True
):
    """Gráfica ejecutiva mensual/acumulada con año en foco y meta acumulada."""
    if monthly.empty:
        st.info("No hay datos para graficar.")
        return

    years = sorted(monthly["Año"].dropna().astype(int).unique().tolist())
    if not years:
        return

    default_focus = globals().get("selected_year", max(years))
    if default_focus not in years:
        default_focus = max(years)

    c_mode, c_year = st.columns([1.0, 1.3])
    with c_mode:
        chart_mode = st.segmented_control(
            "Tipo de lectura",
            options=["Mensual", "Acumulado"],
            default="Mensual",
            selection_mode="single",
            required=True,
            key=f"{key}_chart_mode",
            label_visibility="collapsed",
            width="stretch",
        )
    with c_year:
        if interactive and len(years) > 1:
            focus_year = st.segmented_control(
                "Año en foco",
                options=years,
                default=default_focus,
                selection_mode="single",
                required=True,
                key=f"{key}_focus_year",
                label_visibility="collapsed",
                width="stretch",
            )
        else:
            focus_year = default_focus

    focus_year = int(focus_year)

    chart_data = monthly.copy().sort_values(["Año", "Mes_Num"])
    value_col = ycol
    chart_title = title

    if chart_mode == "Acumulado":
        chart_data["Valor_Grafica"] = chart_data.groupby("Año")[ycol].cumsum()
        value_col = "Valor_Grafica"
        chart_title = (
            title.replace("Ventas mensuales", "Ventas acumuladas")
                 .replace("ventas mensuales", "ventas acumuladas")
        )

    historical_colors = ["#B8C3D1", "#7D8DA3", "#9DAABD", "#66788F"]
    dash_cycle = ["dot", "dash", "dashdot", "longdash"]
    hist_color_map = {}
    h = 0
    for year in years:
        if year != focus_year:
            hist_color_map[year] = historical_colors[h % len(historical_colors)]
            h += 1

    fig = go.Figure()

    focus_data = chart_data[chart_data["Año"] == focus_year].sort_values("Mes_Num")
    if not focus_data.empty:
        fig.add_trace(go.Scatter(
            x=focus_data["Mes_Num"],
            y=focus_data[value_col],
            mode="lines",
            line=dict(color="rgba(18,62,112,.12)", width=11),
            hoverinfo="skip",
            showlegend=False,
        ))

    for idx, year in enumerate(years):
        temp = chart_data[chart_data["Año"] == year].sort_values("Mes_Num")
        if temp.empty:
            continue

        is_focus = year == focus_year
        line_color = "#123E70" if is_focus else hist_color_map.get(year, "#94A3B8")

        fig.add_trace(go.Scatter(
            x=temp["Mes_Num"],
            y=temp[value_col],
            mode="lines+markers",
            name=str(year),
            line=dict(
                color=line_color,
                width=4.5 if is_focus else 2.25,
                dash="solid" if is_focus else dash_cycle[idx % len(dash_cycle)],
            ),
            marker=dict(
                size=10 if is_focus else 6.5,
                color=line_color,
                line=dict(width=1.5 if is_focus else .8, color="#FFFFFF"),
            ),
            opacity=1 if is_focus else .76,
            hovertemplate=f"<b>{year}</b><br>Mes: %{{x}}<br>$%{{y:,.0f}}<extra></extra>",
        ))

        last = temp.iloc[-1]
        fig.add_annotation(
            x=min(int(last["Mes_Num"]) + .16, 12.35),
            y=float(last[value_col]),
            text=f"<b>{year}{' · EN FOCO' if is_focus else ''}</b>",
            showarrow=False,
            xanchor="left",
            font=dict(size=10, color=line_color),
            bgcolor="rgba(238,246,255,.96)" if is_focus else "rgba(255,255,255,.90)",
            bordercolor="#B7CFEA" if is_focus else "rgba(148,163,184,.30)",
            borderwidth=1,
            borderpad=4,
        )

    if chart_mode == "Acumulado" and target_map:
        focus_target = float(target_map.get(focus_year, 0) or 0)
        if focus_target > 0:
            tx = list(range(1,13))
            ty = [focus_target * m for m in tx]
            fig.add_trace(go.Scatter(
                x=tx, y=ty,
                mode="lines",
                name=f"Meta acumulada {focus_year}",
                line=dict(color="#64748B", width=2.2, dash="dash"),
                hovertemplate="<b>Meta acumulada</b><br>Mes: %{x}<br>$%{y:,.0f}<extra></extra>",
            ))

    fig.update_layout(
        title=chart_title,
        hovermode="x unified",
        transition=dict(duration=260, easing="cubic-in-out"),
        legend=dict(orientation="h", yanchor="bottom", y=1.03, xanchor="right", x=1, title=None),
    )
    fig.update_xaxes(
        tickmode="array",
        tickvals=list(range(1,13)),
        ticktext=MONTH_ORDER,
        range=[.65,12.7],
    )
    style_exec_chart(fig, height=430, money_axis=True, legend=True)

    st.plotly_chart(
        fig,
        use_container_width=True,
        config=PLOT_CONFIG,
        key=f"{key}_{chart_mode}_{focus_year}",
    )

    if chart_mode == "Acumulado":
        st.caption(
            f"📈 {focus_year} en foco · La línea punteada representa la meta acumulada. "
            "Esta lectura muestra si el año se acerca o se aleja del plan conforme avanzan los meses."
        )
    else:
        st.caption(f"🎯 {focus_year} en foco · Los otros años permanecen visibles como contexto histórico.")

    if not interactive or not show_explorer:
        return

    available_months = sorted(
        monthly.loc[monthly["Año"] == focus_year, "Mes_Num"].dropna().astype(int).unique().tolist()
    )
    if not available_months:
        return

    explore_month = st.segmented_control(
        "Mes a explorar",
        options=available_months,
        default=max(available_months),
        selection_mode="single",
        required=True,
        format_func=lambda m: MONTHS_ES.get(int(m), str(m)),
        key=f"{key}_explore_month_{focus_year}",
        label_visibility="collapsed",
        width="stretch",
    )
    if explore_month is not None:
        render_month_drilldown(df, focus_year, int(explore_month), detail_label)


def monthly_chart(
    df, title, ycol="Ventas_MXN", key=None, interactive=True,
    detail_label="Detalle mensual", target_map=None, show_explorer=True
):
    if df.empty:
        st.info("No hay datos para graficar.")
        return

    monthly = df.groupby(["Año", "Mes_Num"], as_index=False).agg(
        Ventas_MXN=("Ventas_MXN", "sum"),
        Utilidad_Bruta_MXN=("Utilidad_Bruta_MXN", "sum")
    )
    monthly["Año"] = monthly["Año"].astype(int)
    monthly["Mes_Num"] = monthly["Mes_Num"].astype(int)
    monthly["Mes"] = monthly["Mes_Num"].map(MONTHS_ES)

    render_month_chart_fragment(
        df=df,
        monthly=monthly,
        title=title,
        ycol=ycol,
        key=key or "monthly_chart",
        detail_label=detail_label,
        interactive=interactive,
        target_map=target_map,
        show_explorer=show_explorer,
    )


def render_month_drilldown(df, year, month, label="Detalle mensual"):
    if year is None:
        year = globals().get("selected_year")
    if year is None or month is None:
        return
    detail = df[(df["Año"] == int(year)) & (df["Mes_Num"] == int(month))].copy()
    if detail.empty:
        return

    ventas = float(detail["Ventas_MXN"].sum())
    utilidad = float(detail["Utilidad_Bruta_MXN"].sum())
    margen = (utilidad / ventas * 100) if ventas else 0
    clientes = int(detail["Cliente"].nunique()) if "Cliente" in detail.columns else 0
    operaciones = int(len(detail))
    top_client = "Sin dato"
    top_client_amount = 0.0
    if "Cliente" in detail.columns:
        top = detail.groupby("Cliente", as_index=False)["Ventas_MXN"].sum().sort_values("Ventas_MXN", ascending=False)
        if not top.empty:
            top_client = str(top.iloc[0]["Cliente"])
            top_client_amount = float(top.iloc[0]["Ventas_MXN"])

    month_label = MONTHS_ES.get(int(month), str(month))
    html = f"""
    <div class="drill-wrap">
        <div class="drill-head">
            <div>
                <div class="drill-title">🔎 {label} · {month_label} {int(year)}</div>
                <div class="drill-sub">Periodo seleccionado en el Explorador Mensual. El panel se actualiza automáticamente.</div>
            </div>
            <div class="drill-badge">EXPLORADOR MENSUAL</div>
        </div>
        <div class="drill-grid">
            <div class="drill-tile"><div class="drill-label">Ventas</div><div class="drill-value">{fmt_money(ventas)}</div><div class="drill-note">Ingreso del mes</div></div>
            <div class="drill-tile"><div class="drill-label">Utilidad bruta</div><div class="drill-value">{fmt_money(utilidad)}</div><div class="drill-note">Margen {fmt_pct(margen)}</div></div>
            <div class="drill-tile"><div class="drill-label">Clientes</div><div class="drill-value">{clientes:,}</div><div class="drill-note">Clientes únicos</div></div>
            <div class="drill-tile"><div class="drill-label">Operaciones</div><div class="drill-value">{operaciones:,}</div><div class="drill-note">Registros del periodo</div></div>
            <div class="drill-tile"><div class="drill-label">Cliente principal</div><div class="drill-value">{top_client}</div><div class="drill-note">{fmt_money(top_client_amount)}</div></div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_executive_pulse(combined_df, selected_year, months_ytd, fc):
    """Pulso ejecutivo de 10 segundos: crecimiento, mejor mes, margen y ritmo requerido."""
    current = combined_df[(combined_df["Año"] == selected_year) & (combined_df["Mes_Num"].isin(months_ytd))].copy()
    prev_year = selected_year - 1
    previous = combined_df[(combined_df["Año"] == prev_year) & (combined_df["Mes_Num"].isin(months_ytd))].copy()
    curr_sales = float(current["Ventas_MXN"].sum()) if not current.empty else 0
    prev_sales = float(previous["Ventas_MXN"].sum()) if not previous.empty else 0
    yoy_pct = yoy(curr_sales, prev_sales)

    month_sales = current.groupby("Mes_Num", as_index=False)["Ventas_MXN"].sum() if not current.empty else pd.DataFrame()
    if not month_sales.empty:
        best = month_sales.sort_values("Ventas_MXN", ascending=False).iloc[0]
        best_month = MONTHS_ES.get(int(best["Mes_Num"]), "-")
        best_amount = float(best["Ventas_MXN"])
    else:
        best_month, best_amount = "-", 0

    margin = float(fc.get("margen_neto_ytd", 0))
    needed = float(fc.get("venta_req", 0))
    gap = float(fc.get("gap", 0))

    yoy_style = "green" if yoy_pct is not None and yoy_pct >= 0 else "red"
    margin_style = "green" if margin >= 0 else "red"
    needed_style = "green" if gap >= 0 else "yellow"
    yoy_text = fmt_pct(yoy_pct) if yoy_pct is not None else "Sin base"

    html = f"""
    <div class="exec-pulse-grid">
        <div class="exec-pulse {yoy_style}"><div class="exec-pulse-label">Variación YTD vs {prev_year}</div><div class="exec-pulse-value">{yoy_text}</div><div class="exec-pulse-sub">Mismos meses comparables</div></div>
        <div class="exec-pulse"><div class="exec-pulse-label">Mejor mes del periodo</div><div class="exec-pulse-value">{best_month} · {fmt_money(best_amount)}</div><div class="exec-pulse-sub">Mayor ingreso mensual acumulado</div></div>
        <div class="exec-pulse {margin_style}"><div class="exec-pulse-label">Margen neto YTD</div><div class="exec-pulse-value">{fmt_pct(margin)}</div><div class="exec-pulse-sub">Después de gastos administrativos cargados</div></div>
        <div class="exec-pulse {needed_style}"><div class="exec-pulse-label">Ritmo mensual requerido</div><div class="exec-pulse-value">{fmt_money(needed)}</div><div class="exec-pulse-sub">Para alcanzar la meta anual</div></div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def monthly_summary_table(df, title="Resumen mensual de ventas (MXN)", ycol="Ventas_MXN"):
    if df.empty:
        return
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    st.markdown('<div class="table-caption-premium">Valores mensuales por año · importes en MXN · incluye columna total para conciliación rápida.</div>', unsafe_allow_html=True)
    monthly = (
        df.groupby(["Año", "Mes_Num"], as_index=False)[ycol]
        .sum()
        .pivot(index="Año", columns="Mes_Num", values=ycol)
        .fillna(0)
    )
    for m in range(1, 13):
        if m not in monthly.columns:
            monthly[m] = 0
    monthly = monthly[[1,2,3,4,5,6,7,8,9,10,11,12]]
    monthly["Total"] = monthly.sum(axis=1)
    monthly = monthly.rename(columns=MONTHS_ES)
    monthly = monthly.reindex([y for y in VALID_YEARS if y in monthly.index])

    headers = ["Año"] + MONTH_ORDER + ["Total"]
    rows = []
    for year, row in monthly.iterrows():
        tr_class = ' class="highlight-row"' if int(year) == selected_year else ''
        tds = [f"<td>{int(year)}</td>"]
        for col in MONTH_ORDER:
            val = row.get(col, 0)
            tds.append(f"<td>{fmt_money(val) if pd.notna(val) and abs(float(val)) > 0.0001 else '-'}</td>")
        tds.append(f"<td class='total-col'>{fmt_money(row.get('Total', 0))}</td>")
        rows.append(f"<tr{tr_class}>" + "".join(tds) + "</tr>")
    html = """
    <div class="premium-table-wrap">
        <table class="premium-table">
            <thead><tr>{headers}</tr></thead>
            <tbody>{rows}</tbody>
        </table>
    </div>
    """.format(
        headers="".join(f"<th>{h}</th>" for h in headers),
        rows="".join(rows)
    )
    st.markdown(html, unsafe_allow_html=True)


def premium_engineer_table(prom_df):
    """Tabla premium HTML estable para Ranking ejecutivo del equipo."""
    if prom_df.empty:
        st.info("No hay datos comparables de ingenieros para el filtro actual.")
        return

    table = prom_df.copy().sort_values("Ventas_MXN", ascending=False).reset_index(drop=True)
    headers = ["Ingeniero", "Ventas", "Utilidad bruta", "Margen", "Meta acumulada", "Avance", "Estado", "Alerta"]
    rows_html = []

    for idx, row in table.iterrows():
        avance = row.get("Cumplimiento_YTD_Pct", 0)
        if pd.notna(avance) and avance >= 100:
            estado = '<span class="status-good">🟢 En meta</span>'
        elif pd.notna(avance) and avance >= 80:
            estado = '<span class="status-warn">🟡 En seguimiento</span>'
        else:
            estado = '<span class="status-bad">🔴 Bajo meta</span>'

        alerta = str(row.get("Alerta", ""))
        if alerta == "Sin alerta":
            alerta_html = '<span class="status-good">Sin alerta</span>'
        elif "Margen" in alerta:
            alerta_html = f'<span class="status-warn">{alerta}</span>'
        else:
            alerta_html = f'<span class="status-bad">{alerta}</span>'

        ingeniero = str(row.get("Promotor", ""))
        if idx == 0:
            ingeniero = "🏆 " + ingeniero
            tr_class = ' class="highlight-row"'
        elif pd.notna(avance) and avance < 80:
            tr_class = ' class="risk-row"'
        elif pd.notna(avance) and avance < 100:
            tr_class = ' class="warn-row"'
        else:
            tr_class = ""

        cells = [
            ingeniero,
            fmt_money(row.get("Ventas_MXN", 0)),
            fmt_money(row.get("Utilidad_Bruta_MXN", 0)),
            fmt_pct(row.get("Margen_Bruto_Pct", 0)),
            fmt_money(row.get("Meta_YTD", 0)),
            fmt_pct(avance),
            estado,
            alerta_html,
        ]
        rows_html.append(f"<tr{tr_class}>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>")

    html = """
    <div class="premium-table-wrap">
        <table class="premium-table engineer-table">
            <thead><tr>{headers}</tr></thead>
            <tbody>{rows}</tbody>
        </table>
    </div>
    """.format(
        headers="".join(f"<th>{h}</th>" for h in headers),
        rows="".join(rows_html)
    )
    st.markdown(html, unsafe_allow_html=True)




def premium_simple_table(df, title, caption="", columns=None, row_class_fn=None):
    """Tabla HTML premium reusable para salidas ejecutivas.
    columns = [(col_original, "Etiqueta", "tipo")] donde tipo: text, money, pct, number
    """
    if df is None or df.empty:
        st.info("No hay datos para mostrar.")
        return

    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    if caption:
        st.markdown(f'<div class="table-caption-premium">{caption}</div>', unsafe_allow_html=True)

    if columns is None:
        columns = [(c, c, "text") for c in df.columns]

    def fmt_cell(value, kind):
        if kind == "money":
            return fmt_money(value)
        if kind == "money_signed":
            return fmt_money_signed(value)
        if kind == "pct":
            return fmt_pct(value)
        if kind == "number":
            try:
                return f"{float(value):,.0f}"
            except Exception:
                return str(value)
        return "" if pd.isna(value) else str(value)

    rows_html = []
    for idx, row in df.iterrows():
        tr_class = ""
        if row_class_fn is not None:
            cls = row_class_fn(row, idx)
            tr_class = f' class="{cls}"' if cls else ""
        tds = []
        for col, label, kind in columns:
            val = row.get(col, "")
            cell = fmt_cell(val, kind)
            if kind in ["money_signed"] and isinstance(val, (int, float)) and val < 0:
                cell = f'<span class="status-bad">{cell}</span>'
            tds.append(f"<td>{cell}</td>")
        rows_html.append(f"<tr{tr_class}>" + "".join(tds) + "</tr>")

    html = """
    <div class="premium-table-wrap">
        <table class="premium-table">
            <thead><tr>{headers}</tr></thead>
            <tbody>{rows}</tbody>
        </table>
    </div>
    """.format(
        headers="".join(f"<th>{label}</th>" for _, label, _ in columns),
        rows="".join(rows_html)
    )
    st.markdown(html, unsafe_allow_html=True)



def render_executive_summary(consol_fc, proj_fc, store_fc, show_table=True):
    """Vista 0 tipo CEO: lectura ejecutiva sin exceso de gráficas ni scroll."""
    cumplimiento = consol_fc.get("cumplimiento", 0)
    emoji, style, status = status_from_pct(cumplimiento)
    gap = consol_fc.get("gap", 0)
    gap_label, gap_style, _ = gap_label_and_style(gap)
    ventas = consol_fc.get("ventas_ytd", 0)
    proj_share = (proj_fc.get("ventas_ytd", 0) / ventas * 100) if ventas else 0
    store_share = (store_fc.get("ventas_ytd", 0) / ventas * 100) if ventas else 0
    monthly_needed = consol_fc.get("venta_req", 0)
    progress_width = max(0, min(float(cumplimiento), 100))

    if proj_fc.get("cumplimiento", 0) < store_fc.get("cumplimiento", 0):
        risk_unit = "Proyectos"
        risk_pct = proj_fc.get("cumplimiento", 0)
    else:
        risk_unit = "Tienda"
        risk_pct = store_fc.get("cumplimiento", 0)

    html = f"""
    <div class="exec-summary-wrap">
        <div class="exec-summary-title">🏠 Estado General INTEREY</div>
        <div class="exec-summary-sub">Vista CEO: resultado actual, avance proyectado, utilidad estimada, faltante y oportunidad mensual.</div>
        <div class="exec-progress-card">
            <div class="exec-progress-head">
                <div>
                    <div class="exec-progress-label">Cumplimiento proyectado contra meta anual</div>
                    <div class="exec-progress-value">{fmt_pct(cumplimiento)}</div>
                </div>
                <div class="exec-progress-status">{emoji} {status}<br><span style="font-weight:700;opacity:.82;">{fmt_money(consol_fc.get('forecast_ventas',0))} proyectados</span></div>
            </div>
            <div class="exec-progress-track"><div class="exec-progress-fill" style="width:{progress_width}%;"></div></div>
            <div class="exec-progress-foot">Meta anual consolidada: <b>{fmt_money(consol_fc.get('meta_anual',0))}</b> · {gap_label}: <b>{fmt_money_signed(gap)}</b></div>
        </div>
        <div class="exec-insights-grid">
            <div class="exec-insight">
                <div class="exec-insight-label">Composición</div>
                <div class="exec-insight-value">Proyectos {proj_share:,.1f}% · Tienda {store_share:,.1f}%</div>
                <div class="exec-insight-text">Participación de ingresos acumulados en el periodo seleccionado.</div>
            </div>
            <div class="exec-insight {gap_style}">
                <div class="exec-insight-label">Foco comercial</div>
                <div class="exec-insight-value">{fmt_money_signed(gap)}</div>
                <div class="exec-insight-text">Diferencia estimada entre la proyección de cierre y la meta anual.</div>
            </div>
            <div class="exec-insight {'red' if consol_fc.get('utilidad_neta_proy',0) < 0 else 'green'}">
                <div class="exec-insight-label">Utilidad estimada</div>
                <div class="exec-insight-value">{fmt_money(consol_fc.get('utilidad_neta_proy',0))}</div>
                <div class="exec-insight-text">Basado en tendencia actual de utilidad bruta y gastos cargados.</div>
            </div>
            <div class="exec-insight yellow">
                <div class="exec-insight-label">Oportunidad mensual</div>
                <div class="exec-insight-value">{fmt_money(monthly_needed)}</div>
                <div class="exec-insight-text">Venta promedio mensual requerida para alcanzar la meta anual.</div>
            </div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

    if show_table:
        mini = pd.DataFrame([
            {"Unidad":"🔵 Proyectos", "Ventas":proj_fc["ventas_ytd"], "Participación %":proj_share, "Cumplimiento %":proj_fc.get("cumplimiento",0), "Faltante/Excedente":proj_fc.get("gap",0)},
            {"Unidad":"🟢 Tienda", "Ventas":store_fc["ventas_ytd"], "Participación %":store_share, "Cumplimiento %":store_fc.get("cumplimiento",0), "Faltante/Excedente":store_fc.get("gap",0)},
        ])
        premium_simple_table(
            mini,
            "Mini comparativo ejecutivo",
            "Vista compacta para dirección: aportación de cada unidad y avance proyectado contra su meta.",
            columns=[
                ("Unidad", "Unidad", "text"),
                ("Ventas", "Ventas YTD", "money"),
                ("Participación %", "Participación", "pct"),
                ("Cumplimiento %", "Avance proyectado", "pct"),
                ("Faltante/Excedente", "Faltante / excedente", "money_signed"),
            ],
            row_class_fn=lambda row, idx: "highlight-row" if "Proyectos" in str(row.get("Unidad","")) else ""
        )


def render_dynamic_executive_view(view_name, fc, monthly_target_note="", compact=False):
    """Dirección = 6 KPIs esenciales. Análisis = 10 KPIs completos."""
    _, forecast_style, _ = status_from_pct(fc["cumplimiento"])
    gap_label, gap_style, gap_sub = gap_label_and_style(fc["gap"])
    net_style = "red" if fc["utilidad_neta_ytd"] < 0 else "green"
    net_proj_style = "red" if fc["utilidad_neta_proy"] < 0 else "green"

    if view_name == "Consolidado":
        ventas_label, utilidad_label, gastos_label = "💰 Ventas", "📊 Utilidad bruta", "🧾 Gastos"
        neta_label, forecast_label, meta_label = "🏁 Utilidad neta", "🎯 Forecast cierre", "Meta anual"
        ventas_sub = "Proyectos + Tienda"
        utilidad_sub = f"Margen bruto: {fmt_pct(fc.get('margen_bruto_ytd',0))}"
        gastos_sub = "Administrativos cargados"
        meta_sub = "Objetivo corporativo"
    elif view_name == "Proyectos":
        ventas_label, utilidad_label, gastos_label = "💰 Ventas proyectos", "📊 Utilidad bruta", "🧾 Gasto proyectos"
        neta_label, forecast_label, meta_label = "🏁 Utilidad neta", "🎯 Forecast cierre", "Meta anual proyectos"
        ventas_sub = "Cotizado cliente × TC"
        utilidad_sub = f"Margen bruto: {fmt_pct((fc.get('utilidad_bruta_ytd',0)/fc.get('ventas_ytd',1)*100) if fc.get('ventas_ytd',0) else 0)}"
        gastos_sub = "Administrativos cargados"
        meta_sub = monthly_target_note
    else:
        ventas_label, utilidad_label, gastos_label = "💰 Ventas tienda", "📊 Utilidad tienda", "🧾 Gasto tienda"
        neta_label, forecast_label, meta_label = "🏁 Utilidad neta", "🎯 Forecast cierre", "Meta anual tienda"
        ventas_sub = "Cancelados excluidos"
        utilidad_sub = f"Margen bruto: {fmt_pct((fc.get('utilidad_bruta_ytd',0)/fc.get('ventas_ytd',1)*100) if fc.get('ventas_ytd',0) else 0)}"
        gastos_sub = "Administrativos cargados"
        meta_sub = monthly_target_note

    if compact:
        cols = st.columns(6)
        values = [
            (ventas_label, fmt_money(fc["ventas_ytd"]), ventas_sub, ""),
            (utilidad_label, fmt_money(fc["utilidad_bruta_ytd"]), utilidad_sub, ""),
            (gastos_label, fmt_money(fc["gasto_ytd"]), gastos_sub, "gray"),
            (neta_label, fmt_money(fc["utilidad_neta_ytd"]), f"Margen neto: {fmt_pct(fc['margen_neto_ytd'])}", net_style),
            (forecast_label, fmt_money(fc["forecast_ventas"]), compliance_text(fc["cumplimiento"]), forecast_style),
            (gap_label, fmt_money_signed(fc["gap"]), gap_sub, gap_style),
        ]
        for col, item in zip(cols, values):
            with col:
                st.markdown(card(item[0], item[1], item[2], item[3]), unsafe_allow_html=True)
        return

    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: st.markdown(card(ventas_label, fmt_money(fc["ventas_ytd"]), ventas_sub), unsafe_allow_html=True)
    with c2: st.markdown(card(utilidad_label, fmt_money(fc["utilidad_bruta_ytd"]), utilidad_sub), unsafe_allow_html=True)
    with c3: st.markdown(card(gastos_label, fmt_money(fc["gasto_ytd"]), gastos_sub, "gray"), unsafe_allow_html=True)
    with c4: st.markdown(card(neta_label, fmt_money(fc["utilidad_neta_ytd"]), f"Margen neto: {fmt_pct(fc['margen_neto_ytd'])}", net_style), unsafe_allow_html=True)
    with c5: st.markdown(card(forecast_label, fmt_money(fc["forecast_ventas"]), compliance_text(fc["cumplimiento"]), forecast_style), unsafe_allow_html=True)

    st.markdown('<div class="kpi-spacer"></div>', unsafe_allow_html=True)
    d1,d2,d3,d4,d5 = st.columns(5)
    with d1: st.markdown(card(meta_label, fmt_money(fc["meta_anual"]), meta_sub, "gray"), unsafe_allow_html=True)
    with d2: st.markdown(card(gap_label, fmt_money_signed(fc["gap"]), gap_sub, gap_style), unsafe_allow_html=True)
    venta_req_style = "red" if fc["gap"] < 0 else "green"
    with d3: st.markdown(card("Venta requerida mensual", fmt_money(fc.get("venta_req",0)), f"{int(fc.get('meses_restantes',0))} meses restantes", venta_req_style), unsafe_allow_html=True)
    with d4: st.markdown(card("Utilidad bruta estimada", fmt_money(fc["forecast_utilidad_bruta"]), "Antes de gastos", "gray"), unsafe_allow_html=True)
    with d5: st.markdown(card("Utilidad estimada al cierre", fmt_money(fc["utilidad_neta_proy"]), f"Margen: {fmt_pct(fc['margen_neto_proy'])}", net_proj_style), unsafe_allow_html=True)



def render_backlog_coverage_strip(backlog_df, proj_fc):
    """Lectura compacta de trabajo ganado vs brecha de Proyectos."""
    if backlog_df is None or backlog_df.empty:
        return

    total = float(backlog_df["Importe_Pendiente_MXN"].sum())
    healthy = float(backlog_df.loc[backlog_df["Dias_Abiertos"] <= 90, "Importe_Pendiente_MXN"].sum())
    shortfall = max(-float(proj_fc.get("gap",0) or 0), 0)

    coverage = (total / shortfall * 100) if shortfall else 100.0
    healthy_coverage = (healthy / shortfall * 100) if shortfall else 100.0
    remaining = shortfall - total if shortfall else 0.0

    cov_class = "good" if coverage >= 100 else ("warn" if coverage >= 85 else "bad")
    healthy_class = "good" if healthy_coverage >= 100 else ("warn" if healthy_coverage >= 70 else "bad")

    html = f"""
    <div class="backlog-cover-strip">
        <div class="backlog-cover-main">
            <div class="backlog-cover-kicker">Trabajo ganado</div>
            <div class="backlog-cover-title">Backlog vs brecha proyectada de Proyectos</div>
            <div class="backlog-cover-sub">Cobertura potencial sujeta a convertir OC a facturación dentro del año.</div>
        </div>
        <div class="backlog-cover-cell">
            <div class="backlog-cover-kicker">Brecha</div>
            <div class="backlog-cover-value">{fmt_money_compact(shortfall)}</div>
        </div>
        <div class="backlog-cover-cell">
            <div class="backlog-cover-kicker">Backlog</div>
            <div class="backlog-cover-value">{fmt_money_compact(total)}</div>
        </div>
        <div class="backlog-cover-cell">
            <div class="backlog-cover-kicker">Cobertura total</div>
            <div class="backlog-cover-value {cov_class}">{coverage:,.1f}%</div>
        </div>
        <div class="backlog-cover-cell">
            <div class="backlog-cover-kicker">Cobertura ≤90 días</div>
            <div class="backlog-cover-value {healthy_class}">{healthy_coverage:,.1f}%</div>
            <div class="backlog-cover-sub">{'Brecha cubierta' if remaining <= 0 else 'Aún faltan ' + fmt_money_compact(max(remaining,0))}</div>
        </div>
    </div>
    """
    st.html(html)


def render_backlog_view(backlog_df, annual_project_target, project_gap=None):
    """
    Backlog Ejecutivo 2.0.

    Además de antigüedad y concentración, conecta el ingreso comprometido
    con la brecha proyectada de Proyectos para responder:
    ¿el trabajo ya ganado alcanza para cubrir la meta o todavía hay que vender más?
    """
    st.markdown('<div class="section-title">📋 Backlog Ejecutivo</div>', unsafe_allow_html=True)
    trend_note(
        "OC aprobadas en ejecución y pendientes de facturación. "
        "El backlog representa ingreso comprometido, no facturación realizada."
    )

    if backlog_df is None or backlog_df.empty:
        st.info("No hay información de backlog. Carga el CSV en la barra lateral o agrega el archivo base en GitHub.")
        return

    total = float(backlog_df["Importe_Pendiente_MXN"].sum())
    abiertos = int(len(backlog_df))
    promedio = float(backlog_df["Dias_Abiertos"].mean()) if abiertos else 0

    oldest_idx = backlog_df["Dias_Abiertos"].idxmax()
    oldest = backlog_df.loc[oldest_idx]
    oldest_days = int(oldest["Dias_Abiertos"])
    oldest_client = str(oldest.get("Cliente", "Sin cliente"))
    oldest_amount = float(oldest.get("Importe_Pendiente_MXN", 0))

    critical = backlog_df[backlog_df["Dias_Abiertos"] > 90].copy()
    critical_count = int(len(critical))
    critical_amount = float(critical["Importe_Pendiente_MXN"].sum()) if critical_count else 0
    risk_pct = (critical_amount / total * 100) if total else 0

    # Backlog con antigüedad <= 90 días: lectura conservadora de cobertura.
    healthy_backlog = backlog_df[backlog_df["Dias_Abiertos"] <= 90].copy()
    healthy_amount = float(healthy_backlog["Importe_Pendiente_MXN"].sum()) if not healthy_backlog.empty else 0

    annual_coverage_pct = (total / annual_project_target * 100) if annual_project_target else 0

    # Brecha proyectada = forecast - meta. Si es negativa, existe faltante.
    try:
        project_gap = float(project_gap) if project_gap is not None else None
    except Exception:
        project_gap = None

    project_shortfall = max(-project_gap, 0) if project_gap is not None else 0
    coverage_gap_pct = (total / project_shortfall * 100) if project_shortfall else 0
    healthy_coverage_pct = (healthy_amount / project_shortfall * 100) if project_shortfall else 0
    remaining_after_backlog = project_shortfall - total if project_shortfall else 0

    client_summary = (
        backlog_df.groupby("Cliente", as_index=False)
        .agg(Importe=("Importe_Pendiente_MXN", "sum"), Proyectos=("Cliente", "size"))
        .sort_values("Importe", ascending=False)
    )
    # Participación de cada cliente dentro del backlog total.
    # La gráfica premium usa esta columna en el hover; debe existir antes del Top 10.
    client_summary["Participacion"] = (
        client_summary["Importe"] / total * 100
        if total else 0.0
    )
    top_client = str(client_summary.iloc[0]["Cliente"]) if not client_summary.empty else "Sin cliente"
    top_client_amount = float(client_summary.iloc[0]["Importe"]) if not client_summary.empty else 0
    top_client_share = (top_client_amount / total * 100) if total else 0

    # ---------- LECTURA DE COBERTURA ----------
    if project_shortfall > 0:
        if coverage_gap_pct >= 100:
            coverage_class = "good"
            coverage_status = "Cobertura suficiente"
            surplus = abs(remaining_after_backlog)
            headline = "El backlog actual tiene capacidad para cubrir la brecha proyectada de Proyectos."
            headline_sub = (
                f"Backlog pendiente: {fmt_money(total)} · Brecha proyectada: {fmt_money(project_shortfall)}. "
                "La cobertura depende de convertir estas OC a facturación dentro del año."
            )
            action_label = "Escenario si se factura todo el backlog"
            action_text = "La brecha quedaría cubierta y existiría un excedente potencial contra la meta."
            action_value = f"+{fmt_money(surplus)}"
        elif coverage_gap_pct >= 85:
            coverage_class = "warn"
            headline = f"El backlog actual cubre {coverage_gap_pct:,.1f}% de la brecha proyectada de Proyectos."
            headline_sub = (
                f"Backlog pendiente: {fmt_money(total)} · Brecha proyectada: {fmt_money(project_shortfall)}. "
                "Estamos cerca de tener trabajo suficiente, sujeto a su facturación antes del cierre."
            )
            action_label = "Pendiente por generar"
            action_text = "Incluso facturando todo el backlog actual, todavía se requiere venta adicional para cubrir la brecha."
            action_value = fmt_money(max(remaining_after_backlog, 0))
        else:
            coverage_class = "bad"
            headline = f"El backlog actual cubre {coverage_gap_pct:,.1f}% de la brecha proyectada de Proyectos."
            headline_sub = (
                f"Backlog pendiente: {fmt_money(total)} · Brecha proyectada: {fmt_money(project_shortfall)}. "
                "El trabajo ganado aún no es suficiente para sostener la meta proyectada."
            )
            action_label = "Venta adicional requerida"
            action_text = "Se necesita incrementar el pipeline comercial además de convertir el backlog existente."
            action_value = fmt_money(max(remaining_after_backlog, 0))
    else:
        coverage_class = "good"
        headline = "Proyectos no presenta una brecha proyectada contra la meta anual."
        headline_sub = (
            f"El backlog adicional es de {fmt_money(total)} y equivale al {annual_coverage_pct:,.1f}% "
            "de la meta anual de Proyectos."
        )
        action_label = "Prioridad ejecutiva"
        action_text = "Proteger la conversión a facturación y la rentabilidad de los proyectos comprometidos."
        action_value = fmt_money(total)

    risk_class = "bad" if risk_pct >= 35 else ("warn" if risk_pct >= 20 else "good")
    age_class = "bad" if promedio > 90 else ("warn" if promedio > 60 else "good")

    radar_html = f"""
    <div class="backlog-exec">
        <div class="backlog-exec-top">
            <div>
                <div class="backlog-exec-title">📡 Radar del Backlog</div>
                <div class="backlog-exec-kicker">Cobertura de meta · Aging · Riesgo financiero</div>
            </div>
            <div class="backlog-exec-status">
                {('🔴' if risk_pct >= 35 else '🟡' if risk_pct >= 20 else '🟢')}
                RIESGO FINANCIERO · {risk_pct:,.1f}%
            </div>
        </div>

        <div class="backlog-exec-summary">
            <div class="backlog-exec-summary-label">Lectura ejecutiva</div>
            <div class="backlog-exec-summary-title">{headline}</div>
            <div class="backlog-exec-summary-sub">{headline_sub}</div>
        </div>

        <div class="backlog-exec-grid">
            <div class="backlog-exec-metric {coverage_class}">
                <div class="backlog-exec-label">Cobertura de brecha</div>
                <div class="backlog-exec-value">{coverage_gap_pct:,.1f}%</div>
                <div class="backlog-exec-meta">Backlog total vs brecha proyectada de Proyectos</div>
            </div>

            <div class="backlog-exec-metric {'good' if remaining_after_backlog <= 0 else 'warn' if coverage_gap_pct >= 85 else 'bad'}">
                <div class="backlog-exec-label">{'Excedente potencial' if remaining_after_backlog <= 0 else 'Pendiente por generar'}</div>
                <div class="backlog-exec-value">{fmt_money_compact(abs(remaining_after_backlog))}</div>
                <div class="backlog-exec-meta">Después de aplicar el backlog actual contra la brecha</div>
            </div>

            <div class="backlog-exec-metric blue">
                <div class="backlog-exec-label">Cobertura conservadora ≤90 días</div>
                <div class="backlog-exec-value">{healthy_coverage_pct:,.1f}%</div>
                <div class="backlog-exec-meta">{fmt_money(healthy_amount)} de backlog con antigüedad no crítica</div>
            </div>

            <div class="backlog-exec-metric {risk_class}">
                <div class="backlog-exec-label">Exposición &gt;90 días</div>
                <div class="backlog-exec-value">{fmt_money_compact(critical_amount)}</div>
                <div class="backlog-exec-meta">{critical_count:,} proyectos · {risk_pct:,.1f}% del backlog</div>
            </div>
        </div>

        <div class="backlog-exec-action">
            <div>
                <div class="backlog-exec-action-label">{action_label}</div>
                <div class="backlog-exec-action-text">{action_text}</div>
                <div class="backlog-coverage-note">
                    El backlog es ingreso comprometido. La cobertura solo se materializa si los proyectos se facturan dentro del periodo analizado.
                </div>
            </div>
            <div class="backlog-exec-action-value">{action_value}</div>
        </div>
    </div>
    """
    st.html(radar_html)

    # ---------- KPIs OPERATIVOS ----------
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(card("💰 Backlog total", fmt_money(total), "OC aprobadas pendientes de facturar"), unsafe_allow_html=True)
    with c2:
        st.markdown(card("📋 Proyectos abiertos", f"{abiertos:,}", "Actualmente en ejecución", "green"), unsafe_allow_html=True)
    with c3:
        st.markdown(card("⏳ Antigüedad promedio", f"{promedio:,.0f} días", "Desde la recepción de la OC", age_class), unsafe_allow_html=True)
    with c4:
        old_style = "red" if oldest_days > 90 else ("orange" if oldest_days > 60 else "yellow")
        st.markdown(card("Proyecto más antiguo", f"{oldest_days:,} días", f"{oldest_client} · {fmt_money(oldest_amount)}", old_style), unsafe_allow_html=True)

    # ---------- RIESGO FINANCIERO REFINADO ----------
    if critical_count:
        risk_html = f"""
        <div class="backlog-risk-strip">
            <div class="backlog-risk-main">
                <div class="backlog-risk-label">Riesgo financiero detectado</div>
                <div class="backlog-risk-title">El aging crítico requiere seguimiento para proteger la conversión a facturación.</div>
            </div>
            <div class="backlog-risk-cell bad">
                <div class="backlog-risk-cell-label">Proyectos &gt;90 días</div>
                <div class="backlog-risk-cell-value">{critical_count:,}</div>
            </div>
            <div class="backlog-risk-cell bad">
                <div class="backlog-risk-cell-label">Importe expuesto</div>
                <div class="backlog-risk-cell-value">{fmt_money_compact(critical_amount)}</div>
            </div>
            <div class="backlog-risk-cell">
                <div class="backlog-risk-cell-label">% del backlog</div>
                <div class="backlog-risk-cell-value">{risk_pct:,.1f}%</div>
            </div>
        </div>
        """
        st.html(risk_html)
    else:
        st.success("✅ Backlog sano: no existen proyectos con más de 90 días de antigüedad.")

    # ---------- AGING ----------
    order = ["🟢 0–30 días", "🟡 31–60 días", "🟠 61–90 días", "🔴 Más de 90 días"]
    aging = backlog_df.groupby("Antigüedad", as_index=False).agg(
        Proyectos=("Antigüedad", "size"),
        Importe=("Importe_Pendiente_MXN", "sum")
    )
    aging["Antigüedad"] = pd.Categorical(aging["Antigüedad"], categories=order, ordered=True)
    aging = aging.sort_values("Antigüedad")
    aging["Participacion"] = (aging["Importe"] / total * 100) if total else 0

    st.markdown('<div class="section-title">Aging del backlog</div>', unsafe_allow_html=True)

    a1, a2, a3, a4 = st.columns(4)
    age_cards = [
        ("🟢 0–30 días", "green"),
        ("🟡 31–60 días", "yellow"),
        ("🟠 61–90 días", "orange"),
        ("🔴 Más de 90 días", "red")
    ]
    for col, (bucket, style) in zip([a1, a2, a3, a4], age_cards):
        row = aging[aging["Antigüedad"] == bucket]
        count = int(row["Proyectos"].iloc[0]) if not row.empty else 0
        amount = float(row["Importe"].iloc[0]) if not row.empty else 0
        share = float(row["Participacion"].iloc[0]) if not row.empty else 0
        with col:
            st.markdown(card(bucket, f"{count:,} proyectos", f"{fmt_money(amount)} · {share:,.1f}% del backlog", style), unsafe_allow_html=True)

    st.markdown('<div class="section-title">Composición y concentración</div>', unsafe_allow_html=True)
    g1, g2 = st.columns(2)

    with g1:
        age_palette = {
            "🟢 0–30 días": "#73AFA7",
            "🟡 31–60 días": "#C7A45A",
            "🟠 61–90 días": "#C97C45",
            "🔴 Más de 90 días": "#C95353",
        }
        fig_age = go.Figure()
        for bucket in order:
            row = aging[aging["Antigüedad"] == bucket]
            amount = float(row["Importe"].iloc[0]) if not row.empty else 0
            count = int(row["Proyectos"].iloc[0]) if not row.empty else 0
            share = float(row["Participacion"].iloc[0]) if not row.empty else 0
            name_clean = bucket.replace("🟢 ","").replace("🟡 ","").replace("🟠 ","").replace("🔴 ","")
            fig_age.add_trace(go.Bar(
                y=["Backlog"],
                x=[amount],
                name=name_clean,
                orientation="h",
                marker=dict(color=age_palette[bucket], line=dict(width=0)),
                text=[f"{share:.0f}%" if share >= 8 else ""],
                textposition="inside",
                insidetextanchor="middle",
                textfont=dict(color="white", size=12),
                customdata=[[count, share, name_clean]],
                hovertemplate=(
                    "<b>%{customdata[2]}</b><br>"
                    "Importe: $%{x:,.0f}<br>"
                    "Proyectos: %{customdata[0]}<br>"
                    "Participación: %{customdata[1]:.1f}%<extra></extra>"
                ),
            ))
        fig_age.update_layout(
            barmode="stack",
            title="Backlog financiero por antigüedad",
            xaxis_title=None,
            yaxis_title=None,
            bargap=0.35,
        )
        style_exec_chart(fig_age, height=350, money_axis=False, legend=True)
        fig_age.update_xaxes(tickprefix="$", tickformat=",.0f", showgrid=True, gridcolor="#EEF2F7")
        fig_age.update_yaxes(showgrid=False)
        st.plotly_chart(fig_age, use_container_width=True, config=PLOT_CONFIG)
        st.markdown('<div class="chart-caption-premium">La lectura rápida se centra en cuánto del backlog está sano, en seguimiento o en zona crítica.</div>', unsafe_allow_html=True)

    with g2:
        top_clients = client_summary.head(10).copy().reset_index(drop=True)
        top_clients["Rank"] = top_clients.index + 1
        top_clients["Cliente_Label"] = top_clients.apply(lambda r: f'{int(r["Rank"])} · {r["Cliente"]}', axis=1)
        top_clients = top_clients.sort_values("Importe", ascending=True)

        backlog_colors = []
        for _, r in top_clients.iterrows():
            if int(r["Rank"]) == 1:
                backlog_colors.append("#0B1F4D")
            elif int(r["Rank"]) == 2:
                backlog_colors.append("#123E70")
            elif int(r["Rank"]) == 3:
                backlog_colors.append("#2B5D92")
            else:
                backlog_colors.append("#B8C7D9")

        fig_clients = go.Figure(go.Bar(
            x=top_clients["Importe"],
            y=top_clients["Cliente_Label"],
            orientation="h",
            marker=dict(color=backlog_colors),
            text=[fmt_money(v) for v in top_clients["Importe"]],
            textposition="outside",
            cliponaxis=False,
            customdata=list(zip(top_clients["Cliente"], top_clients["Proyectos"], top_clients["Participacion"])),
            hovertemplate="<b>%{customdata[0]}</b><br>Ingreso pendiente: $%{x:,.0f}<br>Proyectos: %{customdata[1]}<br>Participación: %{customdata[2]:.1f}%<extra></extra>",
        ))
        fig_clients.update_layout(title="Clientes con mayor ingreso pendiente")
        style_exec_chart(fig_clients, height=350, money_axis=False, legend=False)
        fig_clients.update_xaxes(tickprefix="$", tickformat=",.0f", showgrid=True, gridcolor="#EEF2F7")
        fig_clients.update_yaxes(showgrid=False)
        st.plotly_chart(fig_clients, use_container_width=True, config=PLOT_CONFIG)
        st.markdown('<div class="chart-caption-premium">Se destacan los clientes con mayor concentración del backlog pendiente de facturación.</div>', unsafe_allow_html=True)

    # ---------- DETALLE MASTER-DETAIL ----------
    render_backlog_detail_fragment(backlog_df)


@st.fragment
def render_backlog_detail_fragment(backlog_df):
    """
    Detalle ejecutivo del Backlog con filtros rápidos y lectura master-detail.
    Solo este bloque se vuelve a ejecutar al cambiar filtros, búsqueda o proyecto.
    """
    st.markdown('<div class="section-title">Detalle ejecutivo de proyectos con OC</div>', unsafe_allow_html=True)
    st.caption(
        "Filtra por antigüedad y abre únicamente el proyecto que necesitas revisar. "
        "El listado prioriza cliente, proyecto, días e importe."
    )

    f1, f2 = st.columns([1.35, 1])
    with f1:
        age_filter = st.segmented_control(
            "Antigüedad",
            options=["Todos", "0–30", "31–60", "61–90", "+90"],
            default="Todos",
            selection_mode="single",
            required=True,
            key="backlog_age_filter_v68",
            label_visibility="collapsed",
            width="stretch",
        )
    with f2:
        search = st.text_input(
            "Buscar",
            placeholder="Buscar # proyecto, cliente, proyecto o responsable…",
            key="backlog_search_v68",
            label_visibility="collapsed",
        )

    filtered = backlog_df.copy()

    if age_filter == "0–30":
        filtered = filtered[filtered["Dias_Abiertos"] <= 30]
    elif age_filter == "31–60":
        filtered = filtered[(filtered["Dias_Abiertos"] >= 31) & (filtered["Dias_Abiertos"] <= 60)]
    elif age_filter == "61–90":
        filtered = filtered[(filtered["Dias_Abiertos"] >= 61) & (filtered["Dias_Abiertos"] <= 90)]
    elif age_filter == "+90":
        filtered = filtered[filtered["Dias_Abiertos"] > 90]

    if search and search.strip():
        q = search.strip().lower()
        haystack = (
            filtered["Numero_Proyecto"].fillna("").astype(str) + " " +
            filtered["Cliente"].fillna("").astype(str) + " " +
            filtered["Proyecto"].fillna("").astype(str) + " " +
            filtered["Responsable"].fillna("").astype(str)
        ).str.lower()
        filtered = filtered[haystack.str.contains(q, regex=False)]

    filtered = filtered.sort_values(
        ["Dias_Abiertos", "Importe_Pendiente_MXN"],
        ascending=[False, False]
    ).copy()

    count = len(filtered)
    amount = float(filtered["Importe_Pendiente_MXN"].sum()) if count else 0

    st.html(f"""
    <div class="backlog-master-summary">
        <div class="backlog-master-summary-main">
            {count:,} proyectos visibles · {fmt_money(amount)} pendientes de facturar
        </div>
        <div class="backlog-master-summary-sub">
            Filtro: {html_lib.escape(str(age_filter))}{' · búsqueda activa' if search and search.strip() else ''}
        </div>
    </div>
    """)

    if filtered.empty:
        st.info("No hay proyectos que coincidan con el filtro actual.")
        return

    def age_visual(days):
        days = int(days)
        if days <= 30:
            return "0–30", "good"
        if days <= 60:
            return "31–60", "warn"
        if days <= 90:
            return "61–90", "attn"
        return "+90", "bad"

    rows = []
    for idx, row in filtered.iterrows():
        age_text, age_class = age_visual(row["Dias_Abiertos"])
        client = html_lib.escape(str(row.get("Cliente", "")))
        project = html_lib.escape(str(row.get("Proyecto", "") or "Sin descripción"))
        days = int(row.get("Dias_Abiertos", 0))
        amount_text = fmt_money(row.get("Importe_Pendiente_MXN", 0))

        numero_raw = row.get("Numero_Proyecto", pd.NA)
        numero_text = f"#{int(numero_raw)}" if pd.notna(numero_raw) else "—"

        rows.append(f"""
        <tr>
            <td class="col-age"><span class="age-pill {age_class}">{age_text}</span></td>
            <td class="col-number"><b>{numero_text}</b></td>
            <td class="col-client"><div class="backlog-client-cell">{client}</div></td>
            <td class="col-project"><div class="backlog-project-two-lines">{project}</div></td>
            <td class="col-days">{days:,}</td>
            <td class="col-amount"><b>{amount_text}</b></td>
        </tr>
        """)

    table_html = f"""
    <div class="backlog-master-wrap">
        <table class="backlog-master-table">
            <thead>
                <tr>
                    <th class="col-age">Aging</th>
                    <th class="col-number"># Proyecto</th>
                    <th class="col-client">Cliente</th>
                    <th class="col-project">Proyecto</th>
                    <th class="col-days">Días</th>
                    <th class="col-amount">Importe</th>
                </tr>
            </thead>
            <tbody>{''.join(rows)}</tbody>
        </table>
    </div>
    """
    st.html(table_html)

    options = filtered.index.tolist()

    def project_option_label(i):
        row = filtered.loc[i]
        project = str(row.get("Proyecto", "") or "Sin descripción").replace("\n", " ").strip()
        if len(project) > 58:
            project = project[:55] + "…"
        numero_raw = row.get("Numero_Proyecto", pd.NA)
        numero_text = f"#{int(numero_raw)}" if pd.notna(numero_raw) else "Sin #"
        return (
            f"{numero_text} · {row.get('Cliente','')} · {project} · "
            f"{int(row.get('Dias_Abiertos',0))} días · {fmt_money(row.get('Importe_Pendiente_MXN',0))}"
        )

    selected_idx = st.selectbox(
        "Abrir detalle del proyecto",
        options=options,
        format_func=project_option_label,
        key=f"backlog_open_project_v68_{age_filter}",
    )

    row = filtered.loc[selected_idx]
    days = int(row.get("Dias_Abiertos", 0))
    age_text, age_class = age_visual(days)
    numero_raw = row.get("Numero_Proyecto", pd.NA)
    numero_text = f"#{int(numero_raw)}" if pd.notna(numero_raw) else "Sin número"
    client = html_lib.escape(str(row.get("Cliente", "") or "Sin cliente"))
    project = html_lib.escape(str(row.get("Proyecto", "") or "Sin descripción"))
    responsible = html_lib.escape(str(row.get("Responsable", "") or "Sin responsable"))
    fecha = row.get("Fecha_OC")
    fecha_text = fecha.strftime("%d/%m/%Y") if pd.notna(fecha) else "Sin fecha"
    amount_text = fmt_money(row.get("Importe_Pendiente_MXN", 0))

    st.html(f"""
    <div class="backlog-detail-panel {age_class}">
        <div class="backlog-detail-kicker">Proyecto seleccionado · Aging {age_text}</div>
        <div class="backlog-detail-title">{client}</div>
        <div class="backlog-detail-project">{project}</div>
        <div class="backlog-detail-grid">
            <div class="backlog-detail-item">
                <div class="backlog-detail-label"># Proyecto</div>
                <div class="backlog-detail-value">{numero_text}</div>
            </div>
            <div class="backlog-detail-item">
                <div class="backlog-detail-label">Responsable</div>
                <div class="backlog-detail-value">{responsible}</div>
            </div>
            <div class="backlog-detail-item">
                <div class="backlog-detail-label">Fecha OC</div>
                <div class="backlog-detail-value">{fecha_text}</div>
            </div>
            <div class="backlog-detail-item">
                <div class="backlog-detail-label">Días abiertos</div>
                <div class="backlog-detail-value">{days:,}</div>
            </div>
            <div class="backlog-detail-item">
                <div class="backlog-detail-label">Importe pendiente</div>
                <div class="backlog-detail-value">{amount_text}</div>
            </div>
        </div>
    </div>
    """)




@st.fragment
def render_engineer_detail_fragment(performance_year, performance_base, project_monthly_target, months_ytd):
    """
    Detalle ejecutivo por ingeniero con comparativo multianual.
    Cambiar ingeniero o año en foco rerenderiza solo este fragmento.
    """
    st.markdown('<div class="section-title">Detalle ejecutivo por ingeniero / promotor</div>', unsafe_allow_html=True)

    current_engineers = sorted(performance_year["Promotor"].dropna().unique().tolist())
    if not current_engineers:
        st.info("No hay ingenieros comparables para el periodo actual.")
        return

    focus = st.selectbox(
        "Selecciona ingeniero / promotor",
        current_engineers,
        key="promotor_detalle_v68"
    )

    history = performance_base[performance_base["Promotor"] == focus].copy()
    years = sorted(history["Año"].dropna().astype(int).unique().tolist())
    if not years:
        st.info("No hay historial disponible para este ingeniero.")
        return

    default_focus_year = selected_year if selected_year in years else max(years)

    st.markdown(
        '<div style="font-size:.70rem;color:#64748B;font-weight:900;'
        'text-transform:uppercase;letter-spacing:.07em;margin-top:4px;">Año en foco</div>',
        unsafe_allow_html=True
    )
    focus_year = st.segmented_control(
        "Año en foco del ingeniero",
        options=years,
        default=default_focus_year,
        selection_mode="single",
        required=True,
        key=f"engineer_focus_year_{focus}",
        label_visibility="collapsed",
        width="content",
    )
    focus_year = int(focus_year)

    # Para una lectura YTD comparable usamos los mismos meses seleccionados.
    focus_period = history[
        (history["Año"] == focus_year) &
        (history["Mes_Num"].isin(months_ytd))
    ].copy()

    # Meta histórica oficial; para el año principal respeta el ajuste actual del dashboard.
    focus_target = (
        float(project_monthly_target)
        if focus_year == selected_year
        else float(PROJECT_TARGETS.get(focus_year, project_monthly_target))
    )

    f_ventas = focus_period["Ventas_MXN"].sum()
    f_util = focus_period["Utilidad_Bruta_MXN"].sum()
    f_margen = f_util / f_ventas * 100 if f_ventas else 0
    f_meta_ytd = focus_target * len(months_ytd)
    f_cump = f_ventas / f_meta_ytd * 100 if f_meta_ytd else 0
    _, f_cump_style, f_cump_status = status_from_pct(f_cump, green=100, yellow=80)

    cdet = st.columns(5)
    with cdet[0]:
        st.markdown(card(f"Ventas · {focus_year}", fmt_money(f_ventas), f"{focus} · meses seleccionados"), unsafe_allow_html=True)
    with cdet[1]:
        st.markdown(card("Utilidad bruta", fmt_money(f_util), f"Margen: {fmt_pct(f_margen)}", "green" if f_util >= 0 else "red"), unsafe_allow_html=True)
    with cdet[2]:
        st.markdown(card("Meta YTD", fmt_money(f_meta_ytd), f"{fmt_money(focus_target)} × {len(months_ytd)} meses", "gray"), unsafe_allow_html=True)
    with cdet[3]:
        st.markdown(card("Cumplimiento YTD", fmt_pct(f_cump), f_cump_status, f_cump_style), unsafe_allow_html=True)
    with cdet[4]:
        st.markdown(card(
            "Diferencia vs meta",
            fmt_money_signed(f_ventas - f_meta_ytd),
            "positivo = arriba de meta",
            "green" if f_ventas >= f_meta_ytd else "red"
        ), unsafe_allow_html=True)

    # ---------- COMPARATIVO MULTIANUAL ----------
    monthly = (
        history.groupby(["Año", "Mes_Num"], as_index=False)
        .agg(
            Ventas_MXN=("Ventas_MXN", "sum"),
            Utilidad_Bruta_MXN=("Utilidad_Bruta_MXN", "sum")
        )
        .sort_values(["Año", "Mes_Num"])
    )
    monthly["Año"] = monthly["Año"].astype(int)

    historical_colors = ["#B8C3D1", "#7D8DA3", "#9DAABD", "#66788F"]
    dash_cycle = ["dot", "dash", "dashdot", "longdash"]
    hist_color_map = {}
    h = 0
    for year in years:
        if year != focus_year:
            hist_color_map[year] = historical_colors[h % len(historical_colors)]
            h += 1

    fig = go.Figure()

    # Halo sutil del año en foco.
    focus_line = monthly[monthly["Año"] == focus_year].sort_values("Mes_Num")
    if not focus_line.empty:
        fig.add_trace(go.Scatter(
            x=focus_line["Mes_Num"],
            y=focus_line["Ventas_MXN"],
            mode="lines",
            line=dict(color="rgba(18,62,112,.12)", width=11),
            hoverinfo="skip",
            showlegend=False,
            legendgroup=str(focus_year),
        ))

    for idx, year in enumerate(years):
        temp = monthly[monthly["Año"] == year].sort_values("Mes_Num")
        if temp.empty:
            continue

        is_focus = year == focus_year
        line_color = "#123E70" if is_focus else hist_color_map.get(year, "#94A3B8")
        line_width = 4.5 if is_focus else 2.25
        line_dash = "solid" if is_focus else dash_cycle[idx % len(dash_cycle)]
        marker_size = 10 if is_focus else 6.5

        fig.add_trace(go.Scatter(
            x=temp["Mes_Num"],
            y=temp["Ventas_MXN"],
            mode="lines+markers",
            name=str(year),
            legendgroup=str(year),
            line=dict(color=line_color, width=line_width, dash=line_dash),
            marker=dict(
                size=marker_size,
                color=line_color,
                line=dict(width=1.5 if is_focus else .8, color="#FFFFFF"),
            ),
            opacity=1 if is_focus else .76,
            hovertemplate=(
                f"<b>{year}</b><br>"
                "Mes: %{x}<br>"
                "$%{y:,.0f}<extra></extra>"
            ),
        ))

        last = temp.iloc[-1]
        fig.add_annotation(
            x=min(int(last["Mes_Num"]) + .15, 12.30),
            y=float(last["Ventas_MXN"]),
            text=f"<b>{year}{' · EN FOCO' if is_focus else ''}</b>",
            showarrow=False,
            xanchor="left",
            font=dict(size=10, color=line_color),
            bgcolor="rgba(255,255,255,.90)" if not is_focus else "rgba(238,246,255,.96)",
            bordercolor="rgba(148,163,184,.30)" if not is_focus else "#B7CFEA",
            borderwidth=1,
            borderpad=4,
        )

    # Una sola referencia visual sustituye la gráfica redundante de cumplimiento mensual.
    fig.add_hline(
        y=focus_target,
        line_dash="dash",
        line_width=1.7,
        line_color="#64748B",
        annotation_text=f"Meta mensual {focus_year} · {fmt_money(focus_target)}",
        annotation_position="top left",
        annotation_font_color="#64748B",
        annotation_font_size=10,
    )

    fig.update_layout(
        title=f"Ventas mensuales multianual · {focus}",
        hovermode="x unified",
        transition=dict(duration=260, easing="cubic-in-out"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.03,
            xanchor="right",
            x=1,
            title=None,
        ),
    )
    fig.update_xaxes(
        tickmode="array",
        tickvals=list(range(1,13)),
        ticktext=MONTH_ORDER,
        range=[.65,12.65],
    )
    style_exec_chart(fig, height=430, money_axis=True, legend=True)
    st.plotly_chart(
        fig,
        use_container_width=True,
        config=PLOT_CONFIG,
        key=f"engineer_multiyear_{focus}_{focus_year}",
    )
    st.caption(
        f"🎯 {focus_year} está en foco · La línea punteada marca la meta mensual de {fmt_money(focus_target)}. "
        "Los años anteriores permanecen visibles como contexto."
    )

    # ---------- DETALLE MENSUAL DEL AÑO EN FOCO ----------
    detail = (
        history[
            (history["Año"] == focus_year) &
            (history["Mes_Num"].isin(months_ytd))
        ]
        .groupby("Mes_Num", as_index=False)
        .agg(
            Ventas_MXN=("Ventas_MXN", "sum"),
            Utilidad_Bruta_MXN=("Utilidad_Bruta_MXN", "sum")
        )
        .sort_values("Mes_Num")
    )
    detail["Mes"] = detail["Mes_Num"].map(MONTHS_ES)
    detail["Meta_Mensual"] = focus_target
    detail["Diferencia_Meta_MXN"] = detail["Ventas_MXN"] - detail["Meta_Mensual"]
    detail["Cumplimiento_Pct"] = detail["Ventas_MXN"] / focus_target * 100 if focus_target else 0
    detail["Estado"] = detail["Cumplimiento_Pct"].apply(
        lambda x: "Cumplió" if pd.notna(x) and x >= 100
        else ("Cerca" if pd.notna(x) and x >= 80 else "No cumplió")
    )

    show_detail = detail[
        ["Mes","Ventas_MXN","Utilidad_Bruta_MXN","Meta_Mensual",
         "Diferencia_Meta_MXN","Cumplimiento_Pct","Estado"]
    ].copy()

    premium_simple_table(
        show_detail,
        f"Detalle mensual · {focus} · {focus_year}",
        "La línea de meta de la gráfica permite identificar el cumplimiento de un vistazo; la tabla conserva los importes exactos.",
        columns=[
            ("Mes", "Mes", "text"),
            ("Ventas_MXN", "Ventas", "money"),
            ("Utilidad_Bruta_MXN", "Utilidad bruta", "money"),
            ("Meta_Mensual", "Meta mensual", "money"),
            ("Diferencia_Meta_MXN", "Diferencia vs meta", "money_signed"),
            ("Cumplimiento_Pct", "Avance", "pct"),
            ("Estado", "Estado", "text"),
        ],
        row_class_fn=lambda row, idx: (
            "highlight-row" if str(row.get("Estado","")) == "Cumplió"
            else "warn-row" if str(row.get("Estado","")) == "Cerca"
            else "risk-row"
        )
    )




def build_2026_planning_baseline(projects_df, store_df, expenses_df, engineers_current):
    """
    Construye una base 2026 independiente del año seleccionado en el dashboard.
    Ventas/utilidad: anualiza el último periodo disponible de 2026.
    Gastos: anualiza SOLO meses administrativos realmente disponibles.
    """
    months_2026 = ytd_months_for_selected_year(2026, projects_df, store_df)
    months_2026 = [m for m in months_2026 if 1 <= int(m) <= 12]
    sales_month_count = max(len(months_2026), 1)

    p26 = projects_df[
        (projects_df["Año"] == 2026) &
        (projects_df["Mes_Num"].isin(months_2026))
    ].copy() if projects_df is not None and not projects_df.empty else pd.DataFrame()

    s26 = store_df[
        (store_df["Año"] == 2026) &
        (store_df["Mes_Num"].isin(months_2026))
    ].copy() if store_df is not None and not store_df.empty else pd.DataFrame()

    p_sales = float(p26["Ventas_MXN"].sum()) if not p26.empty else 0.0
    s_sales = float(s26["Ventas_MXN"].sum()) if not s26.empty else 0.0
    p_util = float(p26["Utilidad_Bruta_MXN"].sum()) if not p26.empty else 0.0
    s_util = float(s26["Utilidad_Bruta_MXN"].sum()) if not s26.empty else 0.0

    p_forecast = p_sales / sales_month_count * 12
    s_forecast = s_sales / sales_month_count * 12
    p_util_forecast = p_util / sales_month_count * 12
    s_util_forecast = s_util / sales_month_count * 12

    p_margin = p_util / p_sales * 100 if p_sales else 0.0
    s_margin = s_util / s_sales * 100 if s_sales else 0.0

    def known_expense_annualized(unit):
        if expenses_df is None or expenses_df.empty:
            return 0.0, 0

        value_col = "Gasto_Proyectos" if unit == "Proyectos" else "Gasto_Tienda"
        flag_col = "Disponible_Proyectos" if unit == "Proyectos" else "Disponible_Tienda"

        temp = expenses_df[
            (expenses_df["Año"] == 2026) &
            (expenses_df[flag_col] == True)
        ].copy()

        if temp.empty:
            return 0.0, 0

        vals = pd.to_numeric(temp[value_col], errors="coerce").dropna()
        if vals.empty:
            return 0.0, 0

        return float(vals.mean() * 12), int(len(vals))

    p_expense_forecast, p_expense_months = known_expense_annualized("Proyectos")
    s_expense_forecast, s_expense_months = known_expense_annualized("Tienda")

    total_forecast = p_forecast + s_forecast
    total_util_forecast = p_util_forecast + s_util_forecast
    total_expense_forecast = p_expense_forecast + s_expense_forecast

    actual_2024 = 0.0
    actual_2025 = 0.0
    for year in [2024, 2025]:
        p = projects_df.loc[projects_df["Año"] == year, "Ventas_MXN"].sum() if projects_df is not None and not projects_df.empty else 0
        s = store_df.loc[store_df["Año"] == year, "Ventas_MXN"].sum() if store_df is not None and not store_df.empty else 0
        if year == 2024:
            actual_2024 = float(p + s)
        else:
            actual_2025 = float(p + s)

    return {
        "months_2026": months_2026,
        "sales_month_count": sales_month_count,
        "project_forecast": p_forecast,
        "store_forecast": s_forecast,
        "total_forecast": total_forecast,
        "project_margin": p_margin,
        "store_margin": s_margin,
        "project_expense_forecast": p_expense_forecast,
        "store_expense_forecast": s_expense_forecast,
        "total_expense_forecast": total_expense_forecast,
        "expense_months_projects": p_expense_months,
        "expense_months_store": s_expense_months,
        "actual_2024": actual_2024,
        "actual_2025": actual_2025,
        "engineers_current": max(int(engineers_current), 1),
        "is_actual_2026": sales_month_count >= 12,
    }


@st.fragment
def render_planning_2027(projects_df, store_df, expenses_df, engineers_current, display_mode):
    """
    Planeación 2027:
    Dirección define crecimiento y el dashboard lo traduce a metas operativas.
    """
    base = build_2026_planning_baseline(
        projects_df, store_df, expenses_df, engineers_current
    )

    st.markdown(
        """
        <div class="plan27-hero">
            <div class="plan27-kicker">Planeación corporativa 2027</div>
            <div class="plan27-title">De una instrucción directiva a metas operativas</div>
            <div class="plan27-sub">
                Define cuánto debe crecer INTEREY y el dashboard traduce ese objetivo a ventas,
                metas por unidad, carga por ingeniero, rentabilidad y capacidad requerida.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    base_label_forecast = "Cierre real 2026" if base["is_actual_2026"] else "Forecast 2026"
    base_source = st.segmented_control(
        "Base para construir 2027",
        options=[base_label_forecast, "Meta 2026"],
        default=base_label_forecast,
        selection_mode="single",
        required=True,
        key="plan27_base_source",
        width="stretch",
    )

    c1, c2 = st.columns([1.4, .8])
    with c1:
        growth_pct = st.slider(
            "Crecimiento objetivo 2027",
            min_value=0,
            max_value=50,
            value=20,
            step=1,
            key="plan27_growth_pct",
            help="Ejemplo: 20% significa que la meta 2027 será 20% superior a la base 2026 seleccionada."
        )
    with c2:
        engineers_2027 = st.number_input(
            "Ingenieros Proyectos 2027",
            min_value=1,
            max_value=20,
            value=max(int(engineers_current), 1),
            step=1,
            key="plan27_engineers"
        )

    if base_source == "Meta 2026":
        base_project = float(PROJECT_TARGETS[2026]) * 12 * int(engineers_current)
        base_store = float(STORE_TARGETS[2026]) * 12
        base_total = base_project + base_store
        base_name = "Meta 2026"
    else:
        base_project = base["project_forecast"]
        base_store = base["store_forecast"]
        base_total = base["total_forecast"]
        base_name = base_label_forecast

    growth_factor = 1 + growth_pct / 100
    target_project_2027 = base_project * growth_factor
    target_store_2027 = base_store * growth_factor
    target_total_2027 = target_project_2027 + target_store_2027

    monthly_total_2027 = target_total_2027 / 12
    monthly_project_2027 = target_project_2027 / 12
    monthly_store_2027 = target_store_2027 / 12
    monthly_per_engineer = monthly_project_2027 / max(int(engineers_2027), 1)

    current_monthly_per_engineer = (
        base["project_forecast"] / 12 / max(int(engineers_current), 1)
        if base["project_forecast"] else 0
    )
    productivity_ratio = (
        monthly_per_engineer / current_monthly_per_engineer
        if current_monthly_per_engineer else 0
    )
    productivity_change = (productivity_ratio - 1) * 100 if productivity_ratio else 0

    equivalent_engineers = (
        math.ceil(monthly_project_2027 / current_monthly_per_engineer)
        if current_monthly_per_engineer > 0 else int(engineers_2027)
    )

    if productivity_ratio <= 1.05:
        capacity_class = "good"
        capacity_label = "Capacidad sostenible"
        capacity_text = "La meta por ingeniero queda cerca del ritmo 2026."
    elif productivity_ratio <= 1.20:
        capacity_class = "warn"
        capacity_label = "Meta exigente"
        capacity_text = "Requiere elevar productividad comercial o reforzar capacidad."
    else:
        capacity_class = "bad"
        capacity_label = "Meta agresiva"
        capacity_text = "La carga individual supera ampliamente el ritmo 2026."

    # Supuestos financieros editables.
    with st.expander("⚙️ Supuestos financieros 2027", expanded=(display_mode == "Análisis")):
        f1, f2, f3 = st.columns(3)
        with f1:
            margin_projects = st.number_input(
                "Margen bruto Proyectos %",
                min_value=0.0,
                max_value=100.0,
                value=float(round(base["project_margin"], 1)),
                step=0.5,
                key="plan27_margin_projects"
            )
        with f2:
            margin_store = st.number_input(
                "Margen bruto Tienda %",
                min_value=0.0,
                max_value=100.0,
                value=float(round(base["store_margin"], 1)),
                step=0.5,
                key="plan27_margin_store"
            )
        with f3:
            expense_growth = st.number_input(
                "Ajuste gastos 2027 %",
                min_value=-20.0,
                max_value=50.0,
                value=0.0,
                step=1.0,
                key="plan27_expense_growth",
                help="0% mantiene el nivel anualizado 2026; ajústalo según presupuesto."
            )

    gross_profit_2027 = (
        target_project_2027 * margin_projects / 100
        + target_store_2027 * margin_store / 100
    )
    expenses_2027 = base["total_expense_forecast"] * (1 + expense_growth / 100)
    net_profit_2027 = gross_profit_2027 - expenses_2027
    net_margin_2027 = net_profit_2027 / target_total_2027 * 100 if target_total_2027 else 0

    net_class = "good" if net_profit_2027 > 0 else "bad"

    # PUM: la instrucción ya traducida.
    command_html = f"""
    <div class="plan27-command">
        <div class="plan27-command-main">
            <div class="plan27-command-label">Instrucción directiva</div>
            <div class="plan27-command-value">“Crecer {growth_pct}% en 2027”</div>
            <div class="plan27-command-text">
                Base utilizada: {base_name} · {fmt_money(base_total)}.
                Incremento requerido: {fmt_money(target_total_2027 - base_total)}.
            </div>
        </div>
        <div class="plan27-command-cell">
            <div class="plan27-command-label">Meta 2027</div>
            <div class="plan27-command-value">{fmt_money(target_total_2027)}</div>
            <div class="plan27-command-text">Ventas consolidadas anuales</div>
        </div>
        <div class="plan27-command-cell">
            <div class="plan27-command-label">Meta mensual</div>
            <div class="plan27-command-value">{fmt_money(monthly_total_2027)}</div>
            <div class="plan27-command-text">Promedio requerido por mes</div>
        </div>
        <div class="plan27-command-cell">
            <div class="plan27-command-label">Capacidad</div>
            <div class="plan27-command-value">{capacity_label}</div>
            <span class="plan27-status {capacity_class}">
                {productivity_change:+.1f}% vs ritmo por ingeniero 2026
            </span>
        </div>
    </div>
    """
    st.html(command_html)

    cards_html = f"""
    <div class="plan27-grid">
        <div class="plan27-card">
            <div class="plan27-label">Proyectos · meta anual</div>
            <div class="plan27-value">{fmt_money(target_project_2027)}</div>
            <div class="plan27-subvalue">{fmt_money(monthly_project_2027)} mensuales</div>
        </div>
        <div class="plan27-card">
            <div class="plan27-label">Tienda · meta anual</div>
            <div class="plan27-value">{fmt_money(target_store_2027)}</div>
            <div class="plan27-subvalue">{fmt_money(monthly_store_2027)} mensuales</div>
        </div>
        <div class="plan27-card {capacity_class}">
            <div class="plan27-label">Meta mensual por ingeniero</div>
            <div class="plan27-value">{fmt_money(monthly_per_engineer)}</div>
            <div class="plan27-subvalue">{int(engineers_2027)} ingenieros considerados</div>
        </div>
        <div class="plan27-card {net_class}">
            <div class="plan27-label">Utilidad neta estimada</div>
            <div class="plan27-value">{fmt_money(net_profit_2027)}</div>
            <div class="plan27-subvalue">Margen neto estimado: {net_margin_2027:,.1f}%</div>
        </div>
    </div>
    """
    st.html(cards_html)

    capacity_html = f"""
    <div class="plan27-note">
        <b>Lectura de capacidad:</b> con {int(engineers_2027)} ingenieros, cada uno tendría que producir
        aproximadamente <b>{fmt_money(monthly_per_engineer)} al mes</b>.
        A productividad similar a 2026, la estructura equivalente sería de
        <b>{equivalent_engineers} ingenieros</b>. {capacity_text}
    </div>
    """
    st.html(capacity_html)

    # Trayectoria 2024 -> 2027
    history = pd.DataFrame({
        "Periodo": ["2024 Real", "2025 Real", base_label_forecast, "2027 Plan"],
        "Ventas": [
            base["actual_2024"],
            base["actual_2025"],
            base["total_forecast"],
            target_total_2027,
        ]
    })

    colors = ["#CBD5E1", "#94A3B8", "#6F8FB3", "#123E70"]
    fig = go.Figure(go.Bar(
        x=history["Periodo"],
        y=history["Ventas"],
        marker=dict(color=colors),
        text=[fmt_money(v) for v in history["Ventas"]],
        textposition="outside",
        cliponaxis=False,
        hovertemplate="<b>%{x}</b><br>$%{y:,.0f}<extra></extra>"
    ))
    fig.update_layout(title="Trayectoria anual y plan 2027")
    style_exec_chart(fig, height=390, money_axis=True, legend=False)
    fig.update_xaxes(showgrid=False)
    st.plotly_chart(fig, use_container_width=True, config=PLOT_CONFIG)

    # Escenarios comparativos únicamente en Análisis.
    if display_mode == "Análisis":
        st.markdown('<div class="section-title">Escenarios rápidos de crecimiento</div>', unsafe_allow_html=True)
        scenarios = []
        for pct in [5, 10, 15, 20, 25, 30]:
            factor = 1 + pct / 100
            total_s = base_total * factor
            proj_s = base_project * factor
            per_eng_s = proj_s / 12 / max(int(engineers_2027), 1)
            scenarios.append({
                "Escenario": f"+{pct}%",
                "Meta_Anual": total_s,
                "Meta_Mensual": total_s / 12,
                "Meta_Proyecto_Mensual": proj_s / 12,
                "Meta_Ingeniero_Mensual": per_eng_s,
            })

        premium_simple_table(
            pd.DataFrame(scenarios),
            "Comparador de escenarios 2027",
            f"Base: {base_name}. Permite comparar rápidamente qué implica cada nivel de crecimiento.",
            columns=[
                ("Escenario", "Crecimiento", "text"),
                ("Meta_Anual", "Meta anual", "money"),
                ("Meta_Mensual", "Meta mensual", "money"),
                ("Meta_Proyecto_Mensual", "Proyectos / mes", "money"),
                ("Meta_Ingeniero_Mensual", "Por ingeniero / mes", "money"),
            ]
        )

    st.caption(
        f"Base financiera: ventas 2026 con {base['sales_month_count']} meses disponibles; "
        f"gastos Proyectos anualizados con {base['expense_months_projects']} meses cerrados y "
        f"Tienda con {base['expense_months_store']} meses cerrados. "
        "El plan es una herramienta de escenario, no un presupuesto aprobado."
    )



# ---------- SIDEBAR ----------
st.sidebar.markdown("## Fuente de información")
manual_mode = st.sidebar.checkbox(
    "🧪 Modo de pruebas / cargar archivos manualmente",
    value=False,
    help="Desactivado: usa automáticamente los archivos guardados en GitHub."
)

proj_upload = store_upload = expense_upload = backlog_upload = None
if manual_mode:
    st.sidebar.markdown("### Reemplazo temporal")
    proj_upload = st.sidebar.file_uploader("Reporte Proyectos", type=["csv"], key="proj_upload")
    store_upload = st.sidebar.file_uploader("Reporte Tienda", type=["csv"], key="store_upload")
    expense_upload = st.sidebar.file_uploader("Archivo de gastos", type=["xlsx"], key="expense_upload")
    backlog_upload = st.sidebar.file_uploader("Proyectos en ejecución (con OC)", type=["csv"], key="backlog_upload")
else:
    st.sidebar.success("🟢 Modo automático · archivos del repositorio GitHub")

projects = load_projects(proj_upload)
store = load_store(store_upload)
expenses = load_expenses(expense_upload)
backlog = load_backlog(backlog_upload)

if projects.empty and store.empty:
    st.error("No encontré datos. Verifica los archivos maestros en la misma carpeta que interey_v44.py.")
    st.stop()

years_available = sorted(set(
    projects.get("Año", pd.Series(dtype=int)).dropna().astype(int).unique().tolist()
    + store.get("Año", pd.Series(dtype=int)).dropna().astype(int).unique().tolist()
))
years_available = [y for y in years_available if y in VALID_YEARS]
selected_year = st.sidebar.selectbox("Año principal", years_available, index=len(years_available)-1)
compare_years = st.sidebar.multiselect("Años a comparar", years_available, default=years_available)

months_available = ytd_months_for_selected_year(selected_year, projects, store)
period_advanced = st.sidebar.checkbox(
    "🔎 Análisis avanzado de periodo",
    value=False,
    help="Actívalo solo si quieres analizar meses específicos."
)
if period_advanced:
    selected_months = st.sidebar.multiselect(
        "Meses del año principal",
        list(range(1, 13)),
        default=months_available,
        format_func=lambda m: MONTHS_ES[m],
        key=f"meses_avanzado_{selected_year}"
    )
    if not selected_months:
        selected_months = months_available
else:
    selected_months = months_available
    st.sidebar.caption("Periodo automático: " + " · ".join(MONTHS_ES[m] for m in selected_months))

st.sidebar.markdown("## Metas")
engineers = st.sidebar.number_input("Ingenieros proyectos considerados", min_value=1, value=ACTIVE_PROJECT_ENGINEERS_FOR_TARGET, step=1)
project_monthly_target = st.sidebar.number_input(
    f"Meta mensual proyectos {selected_year}", min_value=0.0,
    value=float(PROJECT_TARGETS.get(selected_year, 0)), step=50000.0, format="%.0f"
)
store_monthly_target = st.sidebar.number_input(
    f"Meta mensual tienda {selected_year}", min_value=0.0,
    value=float(STORE_TARGETS.get(selected_year, 0)), step=25000.0, format="%.0f"
)

months_ytd = selected_months
project_expenses = expenses_dict(expenses, selected_year, months_ytd, "Proyectos")
store_expenses = expenses_dict(expenses, selected_year, months_ytd, "Tienda")
missing_proj_exp = expense_missing_months(expenses, selected_year, months_ytd, "Proyectos")
missing_store_exp = expense_missing_months(expenses, selected_year, months_ytd, "Tienda")

st.sidebar.markdown("## Gastos automáticos")
if expenses.empty:
    st.sidebar.warning("No se cargó archivo de gastos. Los gastos se calcularán en $0.")
else:
    st.sidebar.caption(f"Gasto proyectos YTD: {fmt_money(sum(project_expenses.values()))}")
    st.sidebar.caption(f"Gasto tienda YTD: {fmt_money(sum(store_expenses.values()))}")
    if missing_proj_exp:
        st.sidebar.warning("Proyectos pendiente: " + ", ".join(MONTHS_ES[m] for m in missing_proj_exp))
    if missing_store_exp:
        st.sidebar.warning("Tienda pendiente: " + ", ".join(MONTHS_ES[m] for m in missing_store_exp))

# Filtros base comparativo
projects_base = projects[projects["Año"].isin(compare_years)].copy()
store_base = store[store["Año"].isin(compare_years)].copy()
projects_year = projects_base[(projects_base["Año"] == selected_year) & (projects_base["Mes_Num"].isin(selected_months))].copy()
store_year = store_base[(store_base["Año"] == selected_year) & (store_base["Mes_Num"].isin(selected_months))].copy()
combined_base = pd.concat([projects_base.assign(Unidad="Proyectos"), store_base.assign(Unidad="Tienda")], ignore_index=True, sort=False)
combined_year = pd.concat([projects_year.assign(Unidad="Proyectos"), store_year.assign(Unidad="Tienda")], ignore_index=True, sort=False)

proj_fc = forecast_block("Proyectos", projects_year, project_expenses, project_monthly_target, months_ytd, multiplier=engineers)
store_fc = forecast_block("Tienda", store_year, store_expenses, store_monthly_target, months_ytd, multiplier=1)
consol_fc = {
    "ventas_ytd": proj_fc["ventas_ytd"] + store_fc["ventas_ytd"],
    "utilidad_bruta_ytd": proj_fc["utilidad_bruta_ytd"] + store_fc["utilidad_bruta_ytd"],
    "gasto_ytd": proj_fc["gasto_ytd"] + store_fc["gasto_ytd"],
    "utilidad_neta_ytd": proj_fc["utilidad_neta_ytd"] + store_fc["utilidad_neta_ytd"],
    "forecast_ventas": proj_fc["forecast_ventas"] + store_fc["forecast_ventas"],
    "forecast_utilidad_bruta": proj_fc["forecast_utilidad_bruta"] + store_fc["forecast_utilidad_bruta"],
    "gasto_anual_proy": proj_fc["gasto_anual_proy"] + store_fc["gasto_anual_proy"],
    "utilidad_neta_proy": proj_fc["utilidad_neta_proy"] + store_fc["utilidad_neta_proy"],
    "meta_anual": proj_fc["meta_anual"] + store_fc["meta_anual"],
}
consol_fc["margen_neto_ytd"] = consol_fc["utilidad_neta_ytd"] / consol_fc["ventas_ytd"] * 100 if consol_fc["ventas_ytd"] else 0
consol_fc["margen_bruto_ytd"] = consol_fc["utilidad_bruta_ytd"] / consol_fc["ventas_ytd"] * 100 if consol_fc["ventas_ytd"] else 0
consol_fc["margen_neto_proy"] = consol_fc["utilidad_neta_proy"] / consol_fc["forecast_ventas"] * 100 if consol_fc["forecast_ventas"] else 0
consol_fc["cumplimiento"] = consol_fc["forecast_ventas"] / consol_fc["meta_anual"] * 100 if consol_fc["meta_anual"] else 0
consol_fc["gap"] = consol_fc["forecast_ventas"] - consol_fc["meta_anual"]
consol_fc["meses_restantes"] = max(12 - len(months_ytd), 0)
consol_fc["venta_req"] = (consol_fc["meta_anual"] - consol_fc["ventas_ytd"]) / consol_fc["meses_restantes"] if consol_fc["meses_restantes"] else 0

project_target_map = {
    y: (project_monthly_target if y == selected_year else float(PROJECT_TARGETS.get(y,0))) * engineers
    for y in VALID_YEARS
}
store_target_map = {
    y: (store_monthly_target if y == selected_year else float(STORE_TARGETS.get(y,0)))
    for y in VALID_YEARS
}
consol_target_map = {
    y: project_target_map.get(y,0) + store_target_map.get(y,0)
    for y in VALID_YEARS
}

data_status_html = None
if selected_year == 2026:
    sales_month = max(selected_months) if selected_months else None
    proj_known = [m for m in selected_months if m not in missing_proj_exp]
    store_known = [m for m in selected_months if m not in missing_store_exp]
    proj_closed = max(proj_known) if proj_known else None
    store_closed = max(store_known) if store_known else None
    provisional = bool(missing_proj_exp or missing_store_exp)

    data_status_html = f"""
    <div class="data-status-strip">
        <div class="data-status-main">
            <div class="data-status-label">Estado de información</div>
            <div class="data-status-value {'warn' if provisional else 'good'}">
                {'Utilidad neta provisional' if provisional else 'Información cerrada'}
            </div>
        </div>
        <div class="data-status-cell">
            <div class="data-status-label">Ventas</div>
            <div class="data-status-value good">{MONTHS_ES.get(sales_month,'—')} actualizado</div>
        </div>
        <div class="data-status-cell">
            <div class="data-status-label">Gastos Proyectos</div>
            <div class="data-status-value {'warn' if missing_proj_exp else 'good'}">{MONTHS_ES.get(proj_closed,'—')} cerrado</div>
        </div>
        <div class="data-status-cell">
            <div class="data-status-label">Gastos Tienda</div>
            <div class="data-status-value {'warn' if missing_store_exp else 'good'}">{MONTHS_ES.get(store_closed,'—')} cerrado</div>
        </div>
    </div>
    """

# ---------- HEADER ----------
months_label = ", ".join(MONTHS_ES[m] for m in selected_months)
here = Path(__file__).resolve().parent
logo_path = None
for logo_name in ["Logo Interey.png", "Logo_Interey.png", "logo_interey.png", "interey_logo.png"]:
    candidate = here / logo_name
    if candidate.exists():
        logo_path = str(candidate)
        break

st.markdown('<div class="hero-wrap">', unsafe_allow_html=True)
hc1, hc2, hc3 = st.columns([1.25, 5.2, 2.0])
with hc1:
    st.markdown('<div class="logo-box-premium">', unsafe_allow_html=True)
    if logo_path:
        st.image(logo_path, use_container_width=True)
    else:
        st.markdown('<div style="font-weight:900;color:#123E70;font-size:1.4rem;">INTEREY</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
with hc2:
    st.markdown('<div class="hero-kicker">INTEREY 360°</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">Inteligencia Comercial y Financiera</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Soluciones en Telecomunicaciones y Seguridad</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hero-pill"><b>Año principal:</b> {selected_year} &nbsp;|&nbsp; <b>Meses analizados:</b> {months_label}</div>', unsafe_allow_html=True)
with hc3:
    data_max_date = latest_data_date(projects_year, store_year)
    data_max_label = fmt_date_es(data_max_date)
    st.markdown(
        f'<div class="hero-date"><b>Datos actualizados al</b><br>'
        f'<span style="font-size:1.25rem;font-weight:900;color:#0B1F4D;">{data_max_label}</span><br>'
        f'<span>Periodo automático según archivos de ventas</span></div>',
        unsafe_allow_html=True
    )
st.markdown('</div>', unsafe_allow_html=True)
if data_status_html:
    st.html(data_status_html)
radar_interey(consol_fc, proj_fc, store_fc)

# ---------- VISTA EJECUTIVA DINÁMICA · FRAGMENTO ----------
@st.fragment
def render_dashboard_body():
    """
    Navegación principal aislada. Cambiar Resumen/Consolidado/Proyectos/Tienda/Backlog
    vuelve a ejecutar únicamente el cuerpo del dashboard; header, Radar y Pulso permanecen estables.
    """
    view_selected = st.radio(
        "Selecciona vista",
        ["Resumen Ejecutivo", "Consolidado", "Proyectos", "Tienda", "Ingresos Comprometidos", "Planeación 2027"],
        horizontal=True,
        label_visibility="collapsed",
        key="vista_ejecutiva"
    )

    display_mode = st.segmented_control(
        "Nivel de detalle",
        options=["Dirección", "Análisis"],
        default="Dirección",
        selection_mode="single",
        required=True,
        key="display_mode_v62",
        label_visibility="collapsed",
        width="content",
        help="Dirección prioriza lectura rápida. Análisis conserva tablas y detalle operativo."
    )

    if view_selected == "Resumen Ejecutivo":
        render_dynamic_executive_view("Consolidado", consol_fc, "Proyectos + Tienda", compact=(display_mode == "Dirección"))
    elif view_selected == "Consolidado":
        render_dynamic_executive_view("Consolidado", consol_fc, "Proyectos + Tienda", compact=(display_mode == "Dirección"))
    elif view_selected == "Proyectos":
        render_dynamic_executive_view("Proyectos", proj_fc, f"{engineers} ing. × {fmt_money(project_monthly_target)} × 12", compact=(display_mode == "Dirección"))
    elif view_selected == "Tienda":
        render_dynamic_executive_view("Tienda", store_fc, f"{fmt_money(store_monthly_target)} × 12", compact=(display_mode == "Dirección"))

    # ---------- CONTENIDO DINÁMICO CONTROLADO POR LA VISTA MAESTRA ----------
    if view_selected == "Resumen Ejecutivo":
        render_backlog_coverage_strip(backlog, proj_fc)

        st.markdown('<div class="section-title">Trayectoria comercial consolidada</div>', unsafe_allow_html=True)
        monthly_chart(
            combined_base,
            "Ventas consolidadas",
            "Ventas_MXN",
            key="monthly_resumen_executive_v74",
            detail_label="Consolidado",
            target_map=consol_target_map,
            interactive=True,
            show_explorer=False,
        )

        if display_mode == "Análisis":
            render_executive_pulse(combined_base, selected_year, months_ytd, consol_fc)
            render_executive_summary(consol_fc, proj_fc, store_fc, show_table=True)
        else:
            trend_note("Vista Dirección: Radar, seis KPIs esenciales, cobertura del backlog y trayectoria comercial. El detalle operativo permanece en Análisis.")

    elif view_selected == "Consolidado":
        st.markdown('<div class="section-title">Resultado corporativo</div>', unsafe_allow_html=True)
        cumplimiento = float(consol_fc["cumplimiento"] or 0)
        forecast = float(consol_fc["forecast_ventas"] or 0)
        meta = float(consol_fc["meta_anual"] or 0)
        gap = float(consol_fc["gap"] or 0)
        marker_pct = max(0, min(cumplimiento / 150 * 100, 100))
        progress_pct = max(0, min(cumplimiento / 150 * 100, 100))
        if cumplimiento >= 100:
            bullet_state = "good"
            bullet_label = "En línea / arriba de meta"
        elif cumplimiento >= 90:
            bullet_state = "warn"
            bullet_label = "Seguimiento cercano"
        else:
            bullet_state = "bad"
            bullet_label = "Riesgo alto"

        bullet_html = f"""
        <div class="bullet-card">
            <div class="bullet-card-head">
                <div>
                    <div class="bullet-title">Cumplimiento proyectado vs meta consolidada</div>
                    <div class="bullet-sub">Lectura ejecutiva de avance proyectado al cierre contra la meta anual consolidada.</div>
                </div>
                <div class="bullet-value-block">
                    <div class="bullet-value">{cumplimiento:,.1f}%</div>
                    <span class="bullet-status {bullet_state}">{bullet_label}</span>
                </div>
            </div>

            <div class="bullet-track">
                <div class="bullet-zone-red"></div>
                <div class="bullet-zone-amber"></div>
                <div class="bullet-zone-green"></div>
                <div class="bullet-progress" style="width:{progress_pct:.2f}%"></div>
                <div class="bullet-marker" style="left:calc({marker_pct:.2f}% - 1.5px);"></div>
            </div>

            <div class="bullet-scale">
                <span>0%</span><span>90%</span><span>100%</span><span>150%</span>
            </div>

            <div class="bullet-kpis">
                <div class="bullet-mini">
                    <div class="bullet-mini-label">Forecast ventas</div>
                    <div class="bullet-mini-value">{fmt_money(forecast)}</div>
                    <div class="bullet-mini-sub">Proyección de cierre anual</div>
                </div>
                <div class="bullet-mini">
                    <div class="bullet-mini-label">Meta consolidada</div>
                    <div class="bullet-mini-value">{fmt_money(meta)}</div>
                    <div class="bullet-mini-sub">Objetivo anual corporativo</div>
                </div>
                <div class="bullet-mini">
                    <div class="bullet-mini-label">Brecha proyectada</div>
                    <div class="bullet-mini-value">{fmt_money(abs(gap))}</div>
                    <div class="bullet-mini-sub">{'Excedente proyectado' if gap >= 0 else 'Faltante proyectado'}</div>
                </div>
            </div>
        </div>
        """
        # Render directo de HTML para evitar que Markdown interprete
        # la sangría interna del bullet chart como bloque de código.
        st.html(bullet_html)
        trend_note("La utilidad neta ya se resume en las tarjetas superiores; la vista Consolidado conserva únicamente indicadores y tendencias que aportan una lectura corporativa.")

        st.markdown('<div class="section-title">Evolución mensual consolidada</div>', unsafe_allow_html=True)
        monthly_chart(
            combined_base,
            "Ventas mensuales consolidadas",
            "Ventas_MXN",
            key="monthly_consolidado_v56",
            detail_label="Consolidado",
            target_map=consol_target_map
        )
        if display_mode == "Análisis":
            monthly_summary_table(combined_base, "Resumen mensual de ventas consolidadas (MXN)", "Ventas_MXN")


    elif view_selected == "Proyectos":
        st.markdown('<div class="section-title">Unidad de negocio: Proyectos</div>', unsafe_allow_html=True)
        trend_note("Esta vista muestra ventas mensuales, conciliación y desempeño comercial del equipo. Orlando Martínez y Ana Margarita Sahagún suman en KPIs corporativos, pero no participan en el comparativo de ingenieros.")

        monthly_chart(
            projects_base,
            "Ventas mensuales proyectos",
            "Ventas_MXN",
            key="monthly_proyectos_v56",
            detail_label="Proyectos",
            target_map=project_target_map
        )
        if display_mode == "Análisis":
            monthly_summary_table(projects_base, "Resumen mensual de ventas proyectos (MXN)", "Ventas_MXN")

        st.markdown('<div class="section-title">Desempeño Comercial del Equipo</div>', unsafe_allow_html=True)
        performance_year = projects_year[~projects_year["Promotor"].fillna("").str.upper().isin(EXCLUDE_FROM_ENGINEER_ANALYSIS)].copy()
        performance_base = projects_base[~projects_base["Promotor"].fillna("").str.upper().isin(EXCLUDE_FROM_ENGINEER_ANALYSIS)].copy()

        if not performance_year.empty:
            prom = performance_year.groupby("Promotor", as_index=False).agg(
                Ventas_MXN=("Ventas_MXN","sum"),
                Utilidad_Bruta_MXN=("Utilidad_Bruta_MXN","sum"),
                Clientes=("Cliente","nunique"),
                Meses_Con_Venta=("Mes_Num","nunique")
            )
            prom["Margen_Bruto_Pct"] = prom["Utilidad_Bruta_MXN"] / prom["Ventas_MXN"].replace(0,pd.NA) * 100
            prom["Meta_YTD"] = project_monthly_target * len(months_ytd)
            prom["Cumplimiento_YTD_Pct"] = prom["Ventas_MXN"] / prom["Meta_YTD"].replace(0,pd.NA) * 100
            prom["Semaforo"] = prom["Cumplimiento_YTD_Pct"].apply(lambda x: "🟢 Cumple" if pd.notna(x) and x >= 100 else ("🟡 Cerca" if pd.notna(x) and x >= 80 else "🔴 Bajo meta"))

            def prom_alert(row):
                issues = []
                if pd.notna(row["Cumplimiento_YTD_Pct"]) and row["Cumplimiento_YTD_Pct"] < 80:
                    issues.append("Bajo meta YTD")
                if pd.notna(row["Margen_Bruto_Pct"]) and row["Margen_Bruto_Pct"] < 20:
                    issues.append("Margen bajo")
                return ", ".join(issues) if issues else "Sin alerta"

            prom["Alerta"] = prom.apply(prom_alert, axis=1)

            # ---------- LECTURA EJECUTIVA DEL EQUIPO ----------
            ranking = prom.sort_values("Ventas_MXN", ascending=False).reset_index(drop=True)

            leader = ranking.iloc[0]
            best_margin = prom.sort_values("Margen_Bruto_Pct", ascending=False).iloc[0]
            best_compliance = prom.sort_values("Cumplimiento_YTD_Pct", ascending=False).iloc[0]
            on_target = int((prom["Cumplimiento_YTD_Pct"] >= 100).sum())
            team_count = int(len(prom))

            summary_html = f"""
            <div class="team-exec-strip">
                <div class="team-exec-cell">
                    <div class="team-exec-label">Líder en ventas</div>
                    <div class="team-exec-value">{html_lib.escape(str(leader["Promotor"]))}</div>
                    <div class="team-exec-sub">{fmt_money(leader["Ventas_MXN"])} acumulados</div>
                </div>
                <div class="team-exec-cell {'good' if float(best_compliance["Cumplimiento_YTD_Pct"]) >= 100 else 'warn' if float(best_compliance["Cumplimiento_YTD_Pct"]) >= 80 else 'bad'}">
                    <div class="team-exec-label">Mayor cumplimiento</div>
                    <div class="team-exec-value">{fmt_pct(best_compliance["Cumplimiento_YTD_Pct"])}</div>
                    <div class="team-exec-sub">{html_lib.escape(str(best_compliance["Promotor"]))}</div>
                </div>
                <div class="team-exec-cell good">
                    <div class="team-exec-label">Mejor margen bruto</div>
                    <div class="team-exec-value">{fmt_pct(best_margin["Margen_Bruto_Pct"])}</div>
                    <div class="team-exec-sub">{html_lib.escape(str(best_margin["Promotor"]))}</div>
                </div>
                <div class="team-exec-cell {'good' if on_target == team_count and team_count else 'warn' if on_target > 0 else 'bad'}">
                    <div class="team-exec-label">Ingenieros en meta</div>
                    <div class="team-exec-value">{on_target} de {team_count}</div>
                    <div class="team-exec-sub">Cumplimiento YTD ≥ 100%</div>
                </div>
            </div>
            """
            st.html(summary_html)

            # ---------- RANKING EJECUTIVO ----------
            st.markdown('<div class="section-title">Ranking ejecutivo del equipo</div>', unsafe_allow_html=True)
            st.caption("Una sola lectura combina ventas, avance contra meta, utilidad, margen y estado comercial.")

            ranking_rows = []
            for i, row in ranking.iterrows():
                avance = float(row.get("Cumplimiento_YTD_Pct", 0) or 0)
                margen = float(row.get("Margen_Bruto_Pct", 0) or 0)

                if avance >= 100:
                    status_class = "good"
                    status_text = "En meta"
                elif avance >= 80:
                    status_class = "warn"
                    status_text = "Seguimiento"
                else:
                    status_class = "bad"
                    status_text = "Bajo meta"

                progress_width = max(0, min(avance, 100))

                ranking_rows.append(f"""
                <div class="team-ranking-row">
                    <div class="team-rank-number">{i + 1}</div>
                    <div>
                        <div class="team-rank-name">{html_lib.escape(str(row.get("Promotor","")))}</div>
                        <div class="team-rank-secondary">{int(row.get("Clientes",0))} clientes</div>
                    </div>
                    <div>
                        <div class="team-rank-sales">{fmt_money(row.get("Ventas_MXN",0))}</div>
                        <div class="team-rank-secondary">ventas YTD</div>
                    </div>
                    <div>
                        <div class="team-progress-top">
                            <span>Avance vs meta</span>
                            <span class="team-progress-value">{fmt_pct(avance)}</span>
                        </div>
                        <div class="team-progress-track">
                            <div class="team-progress-fill {status_class}" style="width:{progress_width:.1f}%"></div>
                        </div>
                    </div>
                    <div>
                        <div class="team-rank-sales">{fmt_money(row.get("Utilidad_Bruta_MXN",0))}</div>
                        <div class="team-rank-secondary">utilidad · margen {fmt_pct(margen)}</div>
                    </div>
                    <div>
                        <span class="team-status {status_class}">{status_text}</span>
                    </div>
                </div>
                """)

            ranking_html = f"""
            <div class="team-ranking">
                <div class="team-ranking-head">
                    <div>#</div>
                    <div>Ingeniero</div>
                    <div>Ventas</div>
                    <div>Avance</div>
                    <div>Utilidad / margen</div>
                    <div>Estado</div>
                </div>
                {''.join(ranking_rows)}
            </div>
            """
            st.html(ranking_html)

            # ---------- PULSO MENSUAL ----------
            # Sustituye el heatmap saturado por una matriz compacta y sobria.
            prom_month = (
                performance_base[
                    (performance_base["Año"] == selected_year) &
                    (performance_base["Mes_Num"].isin(months_ytd))
                ]
                .groupby(["Promotor","Mes_Num"], as_index=False)
                .agg(
                    Ventas_MXN=("Ventas_MXN","sum"),
                    Utilidad_Bruta_MXN=("Utilidad_Bruta_MXN","sum")
                )
            )
            prom_month["Cumplimiento_Pct"] = (
                prom_month["Ventas_MXN"] / project_monthly_target * 100
                if project_monthly_target else 0
            )

            if display_mode == "Análisis":
                st.markdown('<div class="section-title">Pulso mensual del equipo</div>', unsafe_allow_html=True)
                st.caption("Matriz compacta de cumplimiento mensual. El color funciona solo como señal, no como fondo dominante.")

                pulse_rows = []
                ordered_promoters = ranking["Promotor"].tolist()

                for promoter in ordered_promoters:
                    cells = []
                    for m in months_ytd:
                        match = prom_month[
                            (prom_month["Promotor"] == promoter) &
                            (prom_month["Mes_Num"] == m)
                        ]
                        if match.empty:
                            cells.append('<td><span class="pulse-value"><span class="pulse-dot none"></span>—</span></td>')
                        else:
                            pct = float(match.iloc[0]["Cumplimiento_Pct"])
                            cls = "good" if pct >= 100 else ("warn" if pct >= 80 else "bad")
                            cells.append(
                                f'<td><span class="pulse-value"><span class="pulse-dot {cls}"></span>{pct:,.0f}%</span></td>'
                            )

                    pulse_rows.append(
                        f"<tr><td>{html_lib.escape(str(promoter))}</td>{''.join(cells)}</tr>"
                    )

                pulse_html = f"""
                <div class="team-pulse-wrap">
                    <table class="team-pulse">
                        <thead>
                            <tr>
                                <th>Ingeniero</th>
                                {''.join(f'<th>{MONTHS_ES[m]}</th>' for m in months_ytd)}
                            </tr>
                        </thead>
                        <tbody>
                            {''.join(pulse_rows)}
                        </tbody>
                    </table>
                </div>
                """
                st.html(pulse_html)

            render_engineer_detail_fragment(
                performance_year=performance_year,
                performance_base=performance_base,
                project_monthly_target=project_monthly_target,
                months_ytd=months_ytd,
            )
        else:
            st.info("No hay datos de ingenieros/promotores comparables para el filtro actual. Los KPIs corporativos de Proyectos sí pueden incluir Orlando Martínez y Ana Margarita Sahagún.")

    elif view_selected == "Ingresos Comprometidos":
        render_backlog_view(
            backlog,
            project_monthly_target * 12 * engineers,
            project_gap=proj_fc.get("gap", 0),
        )

    elif view_selected == "Planeación 2027":
        render_planning_2027(
            projects_df=projects,
            store_df=store,
            expenses_df=expenses,
            engineers_current=engineers,
            display_mode=display_mode,
        )

    else:  # Tienda
        st.markdown('<div class="section-title">Unidad de negocio: Tienda</div>', unsafe_allow_html=True)
        trend_note("Esta vista muestra ventas mensuales, conciliación y clientes principales. Tienda usa Total como venta y excluye registros cancelados.")

        monthly_chart(
            store_base,
            "Ventas mensuales tienda",
            "Ventas_MXN",
            key="monthly_tienda_v56",
            detail_label="Tienda",
            target_map=store_target_map
        )
        if display_mode == "Análisis":
            monthly_summary_table(store_base, "Resumen mensual de ventas tienda (MXN)", "Ventas_MXN")

        st.markdown('<div class="section-title">Clientes tienda</div>', unsafe_allow_html=True)
        if not store_year.empty:
            cli = store_year.groupby("Cliente", as_index=False).agg(Ventas_MXN=("Ventas_MXN","sum"), Utilidad_Bruta_MXN=("Utilidad_Bruta_MXN","sum"))
            cli["Margen_Bruto_Pct"] = cli["Utilidad_Bruta_MXN"] / cli["Ventas_MXN"].replace(0,pd.NA) * 100

            top10 = cli.sort_values("Ventas_MXN", ascending=False).head(10).copy().reset_index(drop=True)
            top10["Rank"] = top10.index + 1
            top10["Cliente_Label"] = top10.apply(lambda r: f'{int(r["Rank"])} · {r["Cliente"]}', axis=1)
            top10 = top10.sort_values("Ventas_MXN", ascending=True)

            colors = []
            for _, r in top10.iterrows():
                if int(r["Rank"]) == 1:
                    colors.append("#0B1F4D")
                elif int(r["Rank"]) == 2:
                    colors.append("#123E70")
                elif int(r["Rank"]) == 3:
                    colors.append("#2B5D92")
                else:
                    colors.append("#B8C7D9")

            fig = go.Figure(go.Bar(
                x=top10["Ventas_MXN"],
                y=top10["Cliente_Label"],
                orientation="h",
                marker=dict(color=colors),
                text=[fmt_money(v) for v in top10["Ventas_MXN"]],
                textposition="outside",
                cliponaxis=False,
                customdata=list(zip(top10["Cliente"], top10["Margen_Bruto_Pct"], top10["Utilidad_Bruta_MXN"], top10["Rank"])),
                hovertemplate="<b>%{customdata[0]}</b><br>Ventas: $%{x:,.0f}<br>Utilidad: $%{customdata[2]:,.0f}<br>Margen: %{customdata[1]:.1f}%<br>Posición: %{customdata[3]}<extra></extra>",
            ))
            fig.update_layout(title="Clientes con mayor facturación en Tienda")
            style_exec_chart(fig, height=445, money_axis=False, legend=False)
            fig.update_xaxes(tickprefix="$", tickformat=",.0f", showgrid=True, gridcolor="#EEF2F7")
            fig.update_yaxes(showgrid=False)
            st.plotly_chart(fig, use_container_width=True, config=PLOT_CONFIG)
            st.markdown('<div class="chart-caption-premium">Se destacan los tres clientes con mayor facturación del periodo; el resto funciona como contexto comercial.</div>', unsafe_allow_html=True)

            cli_show = cli.sort_values("Ventas_MXN", ascending=False).head(25).copy()
            premium_simple_table(
                cli_show,
                "Ranking Ejecutivo de Clientes Tienda",
                "Principales clientes por ventas, utilidad y margen dentro del periodo seleccionado.",
                columns=[
                    ("Cliente", "Cliente", "text"),
                    ("Ventas_MXN", "Ventas", "money"),
                    ("Utilidad_Bruta_MXN", "Utilidad", "money"),
                    ("Margen_Bruto_Pct", "Margen", "pct"),
                ],
                row_class_fn=lambda row, idx: "highlight-row" if idx == cli_show.index[0] else ""
            )
        else:
            st.info("No hay datos de tienda para el filtro actual.")

    with st.expander("Auditoría avanzada de datos filtrados"):
        st.caption("Se muestran datos desde 01/ene/2024 hasta la fecha más reciente encontrada en los archivos cargados.")
        if view_selected == "Proyectos":
            cols = [c for c in ["Id","Fecha","Año","Mes_Num","Mes","Promotor","Cliente","Descripcion","Moneda","TC","Tipo_Cambio_Aplicado","Cotizado cliente","Ventas_MXN","Utilidad bruta","Utilidad_Bruta_MXN","Margen_Bruto_Pct"] if c in projects.columns]
            st.dataframe(projects[cols].sort_values("Fecha", ascending=False), use_container_width=True, hide_index=True)
        elif view_selected == "Tienda":
            cols = [c for c in ["Fecha","Año","Mes_Num","Mes","Status","Status_Normalizado","Cliente","Pago","SubTotal","Ventas_MXN","Util $","Utilidad_Bruta_MXN","Margen_Bruto_Pct","Total"] if c in store.columns]
            st.dataframe(store[cols].sort_values("Fecha", ascending=False), use_container_width=True, hide_index=True)
        elif view_selected == "Ingresos Comprometidos":
            if backlog.empty:
                st.info("No hay datos de ingresos comprometidos para auditar.")
            else:
                cols = [c for c in ["Id","Fecha_OC","Dias_Abiertos","Antigüedad","Promotor","Cliente","Descripcion","Moneda","TC","Cotizado cliente","Importe_Pendiente_MXN","Status"] if c in backlog.columns]
                st.dataframe(backlog[cols].sort_values("Dias_Abiertos", ascending=False), use_container_width=True, hide_index=True)
        else:
            cols = [c for c in ["Unidad","Fecha","Año","Mes_Num","Mes","Promotor","Cliente","Ventas_MXN","Utilidad_Bruta_MXN","Margen_Bruto_Pct"] if c in combined_year.columns]
            st.dataframe(combined_year[cols].sort_values(["Unidad","Fecha"], ascending=[True,False]), use_container_width=True, hide_index=True)



render_dashboard_body()

with st.expander("ℹ️ Información metodológica"):
    st.markdown("""
    - Corte automático: desde **01/ene/2024** hasta el último mes con ventas disponible en los archivos maestros.
    - Proyectos usa **Cotizado cliente** para ventas y **Utilidad bruta** para utilidad.
    - Las operaciones en USD de Proyectos se convierten con **TC real por operación**.
    - Tienda usa **Total** para ventas y **Util $** para utilidad.
    - Tienda excluye registros con estatus **Cancelado**.
    - Gastos automáticos desde **GASTOS OPERATIVOS 2026.xlsx**: Proyectos = **RESUMEN / Total general**; Tienda = **GASTOS TIENDA 2026 / fila 2026**.
    - Ingresos comprometidos usa el snapshot vigente de proyectos con **OC aprobada**, en ejecución y pendientes de facturar.
    - La antigüedad se calcula desde la fecha de recepción de la OC hasta la fecha actual.
    - El archivo de ingresos comprometidos **reemplaza** el snapshot anterior; no se acumula históricamente.
    - Navegación y exploradores usan **fragmentos de Streamlit** para actualizar solo el bloque afectado y evitar recargas visuales completas.
    """)

st.caption("Versión v77 · PLANEACIÓN 2027 · FIX · Navegación por fragmentos · Transición suave · Explorador mensual · Gastos validados · Backlog Ejecutivo.")
