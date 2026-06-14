#!/usr/bin/env python3
"""Reassign high-confidence 'Misc' posts to the #223 taxonomy (read-modify-write
categories, drop Misc, add the mapped primary; preserve any other categories).
Records prior categories for rollback. Default dry-run; --execute writes."""
from __future__ import annotations
import argparse, base64, html, json, re, sys, urllib.request, urllib.error, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
ENV = ROOT / "scripts/notion-to-wp/.env"
MISC_ID = 1

RULES = [
 ("Indigenous & Reconciliation in Tech",["indigenous","reconciliation","indigenomics","first nation","land back","nuu-chah","haida"]),
 ("AI Ethics & Philosophy",["ethic","philosoph","consciousness","sentien","moral","the soul","ghost in"]),
 ("Responsible AI & Policy",["policy","governance","regulat","responsible ai","sovereign","ai strategy","ai for all"]),
 ("AI for Journalism & Media",["journalism","journalist"," cbc","broadcast","newsroom"]),
 ("Keynotes & Speaking",["keynote","my talk","slides","speaking at","gave a talk"]),
 ("Conversations & Interviews",["interview","sat down with","conversation with","in conversation","q&a","guesting"]),
 ("Events & Reports",["recap","web summit","hackathon","conference","summit","festival","sxsw","south by"]),
 ("Vancouver AI Ecosystem",["vancouver","british columbia","bc+ai","bc + ai"]),
 ("Generative AI Tools & Workflows",["workflow","prompt","midjourney","stable diffusion"," llm","how to build","a guide to","second brain","agentic","notebooklm"," gpt"]),
 ("AI for Creatives",["creativ","artist","generative art"," ai art","filmmak","musician","design"]),
 ("Creative Technology & Making",["prototyp","maker","hardware","built a","i built","open source","cybernetic"]),
 ("Photography & Visual Storytelling",["photograph","flickr","portrait","camera","headshot","gallery"]),
]

def load_env():
    e={}
    for line in open(ENV):
        line=line.strip()
        if "=" in line and not line.startswith("#"):
            k,v=line.split("=",1); e[k]=v.strip()
    return e

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--execute",action="store_true")
    p.add_argument("--namemap",default="/tmp/category_namemap.json")
    args=p.parse_args()
    e=load_env()
    auth=base64.b64encode(f"{e['WP_USER']}:{e['WP_APP_PASSWORD']}".encode()).decode()
    base="https://kriskrug.co/wp-json/wp/v2"
    NAMEMAP=json.load(open(args.namemap))["namemap"]

    def req(method,path,payload=None):
        r=urllib.request.Request(base+path,
            data=json.dumps(payload).encode() if payload else None,
            headers={"Authorization":f"Basic {auth}","Content-Type":"application/json"},method=method)
        try: return json.load(urllib.request.urlopen(r,timeout=40))
        except urllib.error.HTTPError as ex: return {"_err":ex.code}

    def strip(h): return re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",h or "")).strip()

    # pull all Misc posts
    posts=[]
    page=1
    while True:
        b=req("GET",f"/posts?categories={MISC_ID}&per_page=100&page={page}&status=publish&_fields=id,slug,title,excerpt,categories")
        if not isinstance(b,list) or not b: break
        posts+=b; page+=1
    print(f"{len(posts)} Misc posts", flush=True)

    def classify(post):
        tx=(strip(post['title'].get('rendered') if isinstance(post['title'],dict) else '')+" "+
            strip(post['excerpt'].get('rendered') if isinstance(post['excerpt'],dict) else '')).lower()
        for name,kws in RULES:
            if any(k in tx for k in kws): return name,"high"
        return None,"low"

    mode="live" if args.execute else "dry-run"
    out={"written":0,"skipped_lowconf":0,"failed":0}
    rollback=[]
    for post in posts:
        name,conf=classify(post)
        if conf=="low" or not name:
            out["skipped_lowconf"]+=1; continue
        target=NAMEMAP.get(name)
        if not target:
            out["failed"]+=1; print(f"  no id for {name}",flush=True); continue
        cur=post.get("categories") or []
        new=[c for c in cur if c!=MISC_ID]
        if target not in new: new.append(target)
        if new==cur:
            continue  # nothing changes
        if not args.execute:
            out["written"]+=1; continue
        r=req("POST",f"/posts/{post['id']}",{"categories":new})
        if isinstance(r,dict) and r.get("categories") and target in r["categories"] and MISC_ID not in r["categories"]:
            out["written"]+=1; rollback.append({"id":post['id'],"old":cur,"new":new})
        else:
            out["failed"]+=1; print(f"  FAIL {post['id']} -> {r if isinstance(r,dict) and '_err' in r else 'verify'}",flush=True)
        if out["written"]%50==0 and out["written"]:
            print(f"  ...{out['written']} reassigned",flush=True)

    ts=datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d-%H%M%SZ")
    rep=ROOT/f"docs/current-state/reports/category-reassign-{ts}.md"
    rep.parent.mkdir(parents=True,exist_ok=True)
    lines=[f"# Category reassignment — {mode}","",
           f"- Misc posts: {len(posts)}",
           f"- **reassigned (high-confidence): {out['written']}**",
           f"- held in Misc (low-confidence, for content-read pass): {out['skipped_lowconf']}",
           f"- failed: {out['failed']}","",
           "## Rollback (id: old categories)",""]
    for rb in rollback: lines.append(f"- {rb['id']}: {rb['old']} -> {rb['new']}")
    rep.write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(f"\nSUMMARY [{mode}]: reassigned={out['written']} held_lowconf={out['skipped_lowconf']} failed={out['failed']}",flush=True)
    print(f"report: {rep.relative_to(ROOT)}",flush=True)
    return 1 if out["failed"] else 0

if __name__=="__main__":
    raise SystemExit(main())
