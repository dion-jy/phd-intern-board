#!/usr/bin/env python3
"""Switch the board's ad slots on, one stage at a time.

    # 1. account created, site not yet reviewed: load the AdSense script so
    #    Google can verify the site. No ad box is drawn yet.
    python enable_ads.py --client ca-pub-1234567890123456

    # 2. approved, units created: fill the rail and/or the in-feed slots.
    python enable_ads.py --rail 1234567890
    python enable_ads.py --feed 0987654321 --layout-key "-fb+5w+4e-db+86"

    # back to fully off (no script, no boxes, no request):
    python enable_ads.py --off

Each run edits only the AD object (and the google-adsense-account meta tag) in
index.html, so it is safe to run again with one more value. It prints the
ads.txt line, which must live at the root of the *domain* -- that is the
dion-jy.github.io repo, not this one.
"""
import argparse
import re
import sys

PAGE = "index.html"
META_RE = re.compile(r'\n  <meta name="google-adsense-account" content="[^"]*">')


def set_field(src, name, value):
    pat = re.compile(r'(\n    %s: )"[^"]*"' % name)
    if len(pat.findall(src)) != 1:
        sys.exit("could not find exactly one AD.%s in %s" % (name, PAGE))
    return pat.sub(lambda m: '%s"%s"' % (m.group(1), value), src)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--client", help="publisher id, ca-pub- followed by 16 digits")
    ap.add_argument("--rail", help="data-ad-slot of the display unit for the left rail")
    ap.add_argument("--feed", help="data-ad-slot of the unit between job cards")
    ap.add_argument("--layout-key", help="data-ad-layout-key, only for an In-feed unit")
    ap.add_argument("--off", action="store_true", help="clear every field")
    a = ap.parse_args()

    if a.client and not re.fullmatch(r"ca-pub-\d{16}", a.client):
        sys.exit("--client should look like ca-pub-1234567890123456, got %r" % a.client)
    for flag in ("rail", "feed"):
        v = getattr(a, flag)
        if v and not re.fullmatch(r"\d{6,12}", v):
            sys.exit("--%s should be the numeric data-ad-slot, got %r" % (flag, v))

    src = open(PAGE).read()
    src = META_RE.sub("", src)
    if a.off:
        for f in ("client", "railSlot", "feedSlot", "feedLayoutKey"):
            src = set_field(src, f, "")
    else:
        for f, v in (("client", a.client), ("railSlot", a.rail),
                     ("feedSlot", a.feed), ("feedLayoutKey", a.layout_key)):
            if v is not None:
                src = set_field(src, f, v)

    client = re.search(r'\n    client: "([^"]*)"', src).group(1)
    if client:
        # The meta tag is AdSense's other way of confirming the site; harmless
        # alongside ads.txt and it lets review start before ads.txt is pushed.
        src = src.replace("<head>", '<head>\n  <meta name="google-adsense-account" content="%s">' % client, 1)
    open(PAGE, "w").write(src)

    fields = {f: re.search(r'\n    %s: "([^"]*)"' % f, src).group(1)
              for f in ("client", "railSlot", "feedSlot", "feedLayoutKey")}
    stage = ("off" if not fields["client"] else
             "review only (script loads, no boxes)" if not (fields["railSlot"] or fields["feedSlot"]) else
             "live")
    print("AD now:", fields)
    print("stage :", stage)
    if fields["client"]:
        print("\nads.txt for https://dion-jy.github.io/ads.txt :")
        print("google.com, %s, DIRECT, f08c47fec0942fa0" % fields["client"].replace("ca-", ""))


if __name__ == "__main__":
    main()
