#!/usr/bin/env python3
"""Purge em dashes from the 3 Jetpack SEO meta fields site-wide (KK's hard rule).
Meta-only, allowlisted writes; records prior values. Default dry-run."""
from __future__ import annotations
import argparse, base64, json, sys, urllib.request, urllib.error, datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT/"scripts/notion-to-wp"))
from text_polish import purge_em_dashes  # noqa: E402
KEYS=("jetpack_seo_html_title","advanced_seo_description","jetpack_publicize_message")

def main():
    p=argparse.ArgumentParser(); p.add_argument("--execute",action="store_true"); args=p.parse_args()
    env={}
    for line in open(ROOT/"scripts/notion-to-wp/.env"):
        line=line.strip()
        if "=" in line and not line.startswith("#"):
            k,v=line.split("=",1); env[k]=v.strip()
    auth=base64.b64encode(f"{env['WP_USER']}:{env['WP_APP_PASSWORD']}".encode()).decode()
    base="https://kriskrug.co/wp-json/wp/v2"
    def req(method,path,payload=None):
        r=urllib.request.Request(base+path,data=json.dumps(payload).encode() if payload else None,
            headers={"Authorization":f"Basic {auth}","Content-Type":"application/json"},method=method)
        try: return json.load(urllib.request.urlopen(r,timeout=40))
        except urllib.error.HTTPError: return None
    items=[]
    for kind in ("posts","pages"):
        page=1
        while True:
            b=req("GET",f"/{kind}?status=publish&per_page=100&page={page}&context=edit&_fields=id,meta")
            if not b: break
            items+=[(kind,i) for i in b]; page+=1
    changed=0; rollback={}
    for kind,it in items:
        meta=it.get("meta") or {}
        new={}
        for k in KEYS:
            v=meta.get(k)
            if isinstance(v,str) and "—" in v:
                pv=purge_em_dashes(v)
                if pv!=v: new[k]=pv
        if not new: continue
        changed+=1
        if args.execute:
            rollback[it["id"]]={k:meta.get(k,"") for k in new}
            req("POST",f"/{kind}/{it['id']}",{"meta":new})
    mode="EXECUTE" if args.execute else "DRY-RUN"
    print(f"[{mode}] {len(items)} items scanned, {changed} had em dashes in SEO meta")
    if args.execute:
        ts=datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d-%H%M%SZ")
        json.dump(rollback,open(ROOT/f"docs/current-state/reports/emdash-purge-rollback-{ts}.json","w"))
        print(f"  wrote {changed} fixes; rollback -> docs/current-state/reports/emdash-purge-rollback-{ts}.json")
if __name__=="__main__": raise SystemExit(main())
