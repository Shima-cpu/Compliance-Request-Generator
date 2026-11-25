import io
import html
from datetime import date
import pandas as pd
import streamlit as st

REQUIRED = ['BalanceID','UpdateDate','TransactionType','Transaction Amount USD','Payment System']

def prepare(file):
    df = pd.read_csv(file) if file.name.lower().endswith('.csv') else pd.read_excel(file, dtype={'BalanceID':str,'Wallet':str,'TradingAccount':str})
    df.columns = df.columns.astype(str).str.strip()
    missing = set(REQUIRED)-set(df.columns)
    if missing: raise ValueError('Missing columns: '+', '.join(sorted(missing)))
    df['UpdateDate'] = pd.to_datetime(df['UpdateDate'], errors='coerce')
    df['Transaction Amount USD'] = pd.to_numeric(df['Transaction Amount USD'], errors='coerce')
    df['TransactionType'] = df['TransactionType'].astype(str).str.strip().str.lower()
    df['Payment System'] = df['Payment System'].fillna('(Unknown)').astype(str)
    return df

def breakdown(df, key):
    p = df.groupby([key,'TransactionType'],dropna=False)['Transaction Amount USD'].sum().unstack(fill_value=0).reindex(columns=['deposit','withdrawal'],fill_value=0)
    p.columns=['Total In','Total Out']; p['Net']=p['Total In']-p['Total Out']
    return p.sort_values('Total In',ascending=False)

def render():
    st.subheader('Transaction Analyzer')
    f=st.file_uploader('Upload transaction history',type=['xlsx','csv'],key='ta_upload')
    if not f: return
    try: df=prepare(f)
    except Exception as e: st.error(str(e)); return
    invalid=df['UpdateDate'].isna() | df['Transaction Amount USD'].isna() | ~df['TransactionType'].isin(['deposit','withdrawal']) | (df['Transaction Amount USD']<0)
    if invalid.any(): st.warning(f'{invalid.sum()} invalid or unsupported rows excluded.'); st.dataframe(df.loc[invalid],use_container_width=True)
    df=df.loc[~invalid].copy()
    if df.empty: st.warning('No valid transactions.'); return
    dup=df['BalanceID'].notna() & df['BalanceID'].duplicated(keep=False)
    if dup.any():
        st.warning(f'{dup.sum()} rows share a BalanceID. Review before relying on totals; duplicates are not automatically removed.')
        with st.expander('Duplicate IDs'): st.dataframe(df.loc[dup])
    mode=st.radio('Analysis period',['Last 18 months','Entire period','Custom'],horizontal=True,key='ta_period')
    today=pd.Timestamp(date.today())
    if mode=='Last 18 months': start=today-pd.DateOffset(months=18); end=today
    elif mode=='Entire period': start=df.UpdateDate.min().normalize(); end=df.UpdateDate.max().normalize()
    else:
        dates=st.date_input('Date range',value=(df.UpdateDate.min().date(),df.UpdateDate.max().date()),key='ta_dates')
        if len(dates)!=2: return
        start,end=map(pd.Timestamp,dates)
    st.caption(f'{start:%d.%m.%Y} - {end:%d.%m.%Y} (inclusive)')
    systems=st.multiselect('Payment systems (empty = all)',sorted(df['Payment System'].unique()),key='ta_ps')
    d=df[(df.UpdateDate>=start)&(df.UpdateDate<end+pd.Timedelta(days=1))].copy()
    if systems: d=d[d['Payment System'].isin(systems)]
    if d.empty: st.info('No transactions in this selection.'); return
    p=breakdown(d,'Payment System'); a,b=p[['Total In','Total Out']].sum(); money=lambda n:f'${n:,.2f}'
    c=st.columns(2); c[0].metric('Total In',money(a)); c[1].metric('Total Out',money(b)); c=st.columns(2); c[0].metric('Net deposits',money(a-b)); c[1].metric('Withdrawal / Deposit ratio',f'{b/a:.2%}' if a else 'N/A')
    st.subheader('Payment system breakdown')
    st.caption('Green: deposits | Blue-gray: withdrawals. All bars share the same scale.')
    scale=max(float(p[['Total In','Total Out']].max().max()),1)
    for name,row in p.iterrows():
        bars=''
        for label,color in [('Total In','#299e82'),('Total Out','#8798b5')]:
            value=float(row[label]); width=100*value/scale
            bars+=f'<div style="display:flex;align-items:center;gap:12px;margin:6px 0"><div style="flex:1;background:rgba(128,128,128,.10);border-radius:5px;height:12px"><div style="width:{width:.6f}%;height:12px;background:{color};border-radius:5px"></div></div><span style="min-width:110px;text-align:right;font-variant-numeric:tabular-nums">{money(value)}</span></div>'
        st.markdown(f'<div style="margin:12px 0"><div>{html.escape(str(name))}</div>{bars}</div>',unsafe_allow_html=True)
    st.dataframe(p.style.format('${:,.2f}'),use_container_width=True)
    d['Month']=d.UpdateDate.dt.to_period('M').astype(str)
    monthly=breakdown(d,'Month').sort_index(); st.subheader('Monthly activity'); st.bar_chart(monthly[['Total In','Total Out']])
    if 'Wallet' in d:
        with st.expander('Breakdown by wallet'):
            st.dataframe(breakdown(d,'Wallet').style.format('${:,.2f}'),use_container_width=True)
    summary=f'During the reviewed period ({start:%d.%m.%Y} - {end:%d.%m.%Y}), the client deposited {money(a)} and withdrew {money(b)}. Net deposits amounted to {money(a-b)}.'
    st.text_area('Case summary',summary,key='ta_summary_'+str(hash(summary)))
    out=io.BytesIO()
    with pd.ExcelWriter(out,engine='openpyxl') as writer:
        p.to_excel(writer,sheet_name='Payment systems'); monthly.to_excel(writer,sheet_name='Monthly'); d.to_excel(writer,sheet_name='Transactions',index=False)
    st.download_button('Download Excel analysis',out.getvalue(),'transaction_analysis.xlsx',mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    with st.expander('Analysis notes'):
        st.caption(f"Export coverage: {df.UpdateDate.min():%d.%m.%Y} - {df.UpdateDate.max():%d.%m.%Y}.")
        st.caption('Amounts are taken from Transaction Amount USD. Execution status is not checked; use completed operations only.')
        st.caption('Net deposits are not equivalent to confirmed source of funds or proven redeposits.')
        st.caption('Files are processed in the app session, not saved to Supabase.')
