#!/usr/bin/env python3
"""
clean_epg.py
Single-file script to:
- Keep only a configured channel list (channel id preserved)
- Replace display-name per mapping (callsigns/brand names)
- Clean programme titles (remove Live/New/Repeat, remove bracketed annotations)
- For sports, set title to the matchup (from sub-title or description)
- Build standardized descriptions:
    TV shows -> "<Show> - S#E#. <episode desc> (MM/DD/YYYY)"
    Movies    -> "<Movie>. <desc> (MM/DD/YYYY)"
    Sports    -> "<Team A vs Team B>. <desc> (MM/DD/YYYY)"
- Remove all extra tags except <title> and <desc> (date used to build description then removed)
- Sort channels in the order specified and programmes by channel order + start time
- Input file MUST be named `epg.xml` and output will be `clean_epg.xml`
- Won't overwrite the input file
"""

import xml.etree.ElementTree as ET
import re
import os
from datetime import datetime

# -------------------------------
# Config: channel list (one per line; order matters)
# -------------------------------
keep_channels = [
    "Comet(COMET).us",
    "Laff(LAFF).us",
    "ABC(WMTW).us",
    "FOX(WFXT).us",
    "FOX(WPFO).us",
    "NBC(WBTSCD).us",
    "NBC(WCSH).us",
    "ABC(WCVB).us",
    "NewEnglandCableNews(NECN).us",
    "PBS(HD01).us",
    "CW(WLVI).us",
    "CBS(WBZ).us",
    "WSBK.us",
    "CBS(WGME).us",
    "ION.us",
    "MeTVNetwork(METVN).us",
    "INSPHD(INSPHD).us",
    "GameShowNetwork(GSN).us",
    "FamilyEntertainmentTelevision(FETV).us",
    "Heroes&IconsNetwork(HEROICN).us",
    "TurnerClassicMoviesHD(TCMHD).us",
    "OprahWinfreyNetwork(OWN).us",
    "BET.us",
    "DiscoveryChannel(DSC).us",
    "Freeform(FREEFRM).us",
    "USANetwork(USA).us",
    "NewEnglandSportsNetwork(NESN).us",
    "NewEnglandSportsNetworkPlus(NESNPL).us",
    "NBCSportsBoston(NBCSB).us",
    "ESPN.us",
    "ESPN2.us",
    "ESPNEWS.us",
    "AWealthofEntertainmentHD(AWEHD).us",
    "WEtv(WE).us",
    "OxygenTrueCrime(OXYGEN).us",
    "DisneyChannel(DISN).us",
    "DisneyJunior(DJCH).us",
    "DisneyXD(DXD).us",
    "CartoonNetwork(TOONLSH).us",
    "Nickelodeon(NIK).us",
    "MSNBC.us",
    "CableNewsNetwork(CNN).us",
    "HLN.us",
    "CNBC.us",
    "FoxNewsChannel(FNC).us",
    "LifetimeRealWomen(LRW).us",
    "TNT.us",
    "Lifetime(LIFE).us",
    "LMN.us",
    "TLC.us",
    "AMC.us",
    "Home&GardenTelevisionHD(HGTVD).us",
    "TheTravelChannel(TRAV).us",
    "A&E(AETV).us",
    "FoodNetwork(FOOD).us",
    "Bravo(BRAVO).us",
    "truTV(TRUTV).us",
    "NationalGeographicHD(NGCHD).us",
    "HallmarkChannel(HALL).us",
    "HallmarkFamily(HFM).us",
    "HallmarkMystery(HMYS).us",
    "SYFY.us",
    "AnimalPlanet(APL).us",
    "History(HISTORY).us",
    "TheWeatherChannel(WEATH).us",
    "ParamountNetwork(PAR).us",
    "ComedyCentral(COMEDY).us",
    "FXM.us",
    "FXX.us",
    "FX.us",
    "E!EntertainmentTelevisionHD(EHD).us",
    "AXSTV(AXSTV).us",
    "TVLand(TVLAND).us",
    "TBS.us",
    "VH1.us",
    "MTV-MusicTelevision(MTV).us",
    "CMT(CMTV).us",
    "DestinationAmerica(DEST).us",
    "MagnoliaNetwork(MAGN).us",
    "MagnoliaNetworkHD(Pacific)(MAGNPHD).us",
    "DiscoveryLifeChannel(DLC).us",
    "NationalGeographicWild(NGWILD).us",
    "SmithsonianChannelHD(SMTSN).us",
    "BBCAmerica(BBCA).us",
    "POP(POPSD).us",
    "Crime&InvestigationNetworkHD(CINHD).us",
    "Vice(VICE).us",
    "InvestigationDiscoveryHD(IDHD).us",
    "ReelzChannel(REELZ).us",
    "DiscoveryFamilyChannel(DFC).us",
    "Science(SCIENCE).us",
    "AmericanHeroesChannel(AHC).us",
    "AMC+(AMCPLUS).us",
    "Fuse(FUSE).us",
    "MusicTelevisionHD(MTV2HD).us",
    "IFC.us",
    "FYI(FYISD).us",
    "CookingChannel(COOK).us",
    "Logo(LOGO).us",
    "AdultSwim(ADSM).ca",
    "ANTENNA(KGBTDT).us",
    "CHARGE!(CHARGE).us",
    "FS1.us",
    "FS2.us",
    "NFLNetwork(NFLNET).us",
    "NHLNetwork(NHLNET).us",
    "MLBNetwork(MLBN).us",
    "NBATV(NBATV).us",
    "CBSSportsNetwork(CBSSN).us",
    "Ovation(OVATION).us",
    "UPTV.us",
    "COZITV(COZITV).us",
    "OutdoorChannel(OUTD).us",
    "ASPiRE(ASPRE).us",
    "HBO.us",
    "HBO2(HBOHIT).us",
    "HBOComedy(HBOC).us",
    "HBOSignature(HBODRAM).us",
    "HBOWest(HBOHDP).us",
    "HBOZone(HBOMOV).us",
    "CinemaxHD(MAXHD).us",
    "MoreMAX(MAXHIT).us",
    "ActionMAX(MAXACT).us",
    "5StarMAX(MAXCLAS).us",
    "Paramount+withShowtimeOnDemand(SHOWDM).us",
    "ShowtimeExtreme(SHOWX).us",
    "ShowtimeNext(NEXT).us",
    "ShowtimeShowcase(SHOCSE).us",
    "ShowtimeFamilyzone(FAMZ).us",
    "ShowtimeWomen(WOMEN).us",
    "Starz(STARZ).us",
    "StarzEdge(STZE).us",
    "StarzCinema(STZCI).us",
    "StarzComedy(STZC).us",
    "StarzEncore(STZENC).us",
    "StarzEncoreBlack(STZENBK).us",
    "StarzEncoreClassic(STZENCL).us",
    "StarzEncoreFamily(STZENFM).us",
    "StarzEncoreWesterns(STZENWS).us",
    "StarzKids(STZK).us",
    "StarzEncoreAction(STZENAC).us",
    "ScreenPix(SCRNPIX).us",
    "ScreenPixAction(SCRNACT).us",
    "ScreenPixVoices(SCRNVOI).us",
    "ScreenPixWesterns(SCRNWST).us",
    "MoviePlex(MPLEX).us",
    "MGM+Drive-In(MGMDRV).us",
    "MGM+HD(MGMHD).us",
    "MGM+Hits(MGMHIT).us",
    "SonyMovieChannel(SONY).us",
    "TheMovieChannel(TMC).us",
]

# -------------------------------
# Display name mapping (complete)
# -------------------------------
channel_display_map = {
    "Comet(COMET).us": "Comet",
    "Laff(LAFF).us": "Laff",
    "ABC(WMTW).us": "WMTW",
    "FOX(WFXT).us": "WFXT",
    "FOX(WPFO).us": "WPFO",
    "NBC(WBTSCD).us": "WBTSCD",
    "NBC(WCSH).us": "WCSH",
    "ABC(WCVB).us": "WCVB",
    "NewEnglandCableNews(NECN).us": "NECN",
    "PBS(HD01).us": "PBS",
    "CW(WLVI).us": "WLVI",
    "CBS(WBZ).us": "WBZ",
    "WSBK.us": "WSBK",
    "CBS(WGME).us": "WGME",
    "ION.us": "ION",
    "MeTVNetwork(METVN).us": "MeTV",
    "INSPHD(INSPHD).us": "INSP",
    "GameShowNetwork(GSN).us": "GSN",
    "FamilyEntertainmentTelevision(FETV).us": "FETV",
    "Heroes&IconsNetwork(HEROICN).us": "H&I",
    "TurnerClassicMoviesHD(TCMHD).us": "TCM",
    "OprahWinfreyNetwork(OWN).us": "OWN",
    "BET.us": "BET",
    "DiscoveryChannel(DSC).us": "Discovery",
    "Freeform(FREEFRM).us": "Freeform",
    "USANetwork(USA).us": "USA",
    "NewEnglandSportsNetwork(NESN).us": "NESN",
    "NewEnglandSportsNetworkPlus(NESNPL).us": "NESN+",
    "NBCSportsBoston(NBCSB).us": "NBC Sports Boston",
    "ESPN.us": "ESPN",
    "ESPN2.us": "ESPN2",
    "ESPNEWS.us": "ESPNews",
    "AWealthofEntertainmentHD(AWEHD).us": "AWE",
    "WEtv(WE).us": "WE TV",
    "OxygenTrueCrime(OXYGEN).us": "Oxygen",
    "DisneyChannel(DISN).us": "Disney Channel",
    "DisneyJunior(DJCH).us": "Disney Junior",
    "DisneyXD(DXD).us": "Disney XD",
    "CartoonNetwork(TOONLSH).us": "Cartoon Network",
    "Nickelodeon(NIK).us": "Nickelodeon",
    "MSNBC.us": "MSNBC",
    "CableNewsNetwork(CNN).us": "CNN",
    "HLN.us": "HLN",
    "CNBC.us": "CNBC",
    "FoxNewsChannel(FNC).us": "Fox News",
    "LifetimeRealWomen(LRW).us": "LRW",
    "TNT.us": "TNT",
    "Lifetime(LIFE).us": "Lifetime",
    "LMN.us": "LMN",
    "TLC.us": "TLC",
    "AMC.us": "AMC",
    "Home&GardenTelevisionHD(HGTVD).us": "HGTV",
    "TheTravelChannel(TRAV).us": "Travel Channel",
    "A&E(AETV).us": "A&E",
    "FoodNetwork(FOOD).us": "Food Network",
    "Bravo(BRAVO).us": "Bravo",
    "truTV(TRUTV).us": "truTV",
    "NationalGeographicHD(NGCHD).us": "Nat Geo",
    "HallmarkChannel(HALL).us": "Hallmark",
    "HallmarkFamily(HFM).us": "Hallmark Family",
    "HallmarkMystery(HMYS).us": "Hallmark Mystery",
    "SYFY.us": "SYFY",
    "AnimalPlanet(APL).us": "Animal Planet",
    "History(HISTORY).us": "History",
    "TheWeatherChannel(WEATH).us": "Weather Channel",
    "ParamountNetwork(PAR).us": "Paramount",
    "ComedyCentral(COMEDY).us": "Comedy Central",
    "FXM.us": "FXM",
    "FXX.us": "FXX",
    "FX.us": "FX",
    "E!EntertainmentTelevisionHD(EHD).us": "E!",
    "AXSTV(AXSTV).us": "AXS TV",
    "TVLand(TVLAND).us": "TV Land",
    "TBS.us": "TBS",
    "VH1.us": "VH1",
    "MTV-MusicTelevision(MTV).us": "MTV",
    "CMT(CMTV).us": "CMT",
    "DestinationAmerica(DEST).us": "Destination America",
    "MagnoliaNetwork(MAGN).us": "Magnolia",
    "MagnoliaNetworkHD(Pacific)(MAGNPHD).us": "Magnolia Pacific",
    "DiscoveryLifeChannel(DLC).us": "Discovery Life",
    "NationalGeographicWild(NGWILD).us": "Nat Geo Wild",
    "SmithsonianChannelHD(SMTSN).us": "Smithsonian",
    "BBCAmerica(BBCA).us": "BBC America",
    "POP(POPSD).us": "POP",
    "Crime&InvestigationNetworkHD(CINHD).us": "CI",
    "Vice(VICE).us": "VICE",
    "InvestigationDiscoveryHD(IDHD).us": "ID",
    "ReelzChannel(REELZ).us": "Reelz",
    "DiscoveryFamilyChannel(DFC).us": "Discovery Family",
    "Science(SCIENCE).us": "Science",
    "AmericanHeroesChannel(AHC).us": "AHC",
    "AMC+(AMCPLUS).us": "AMC+",
    "Fuse(FUSE).us": "Fuse",
    "MusicTelevisionHD(MTV2HD).us": "MTV2",
    "IFC.us": "IFC",
    "FYI(FYISD).us": "FYI",
    "CookingChannel(COOK).us": "Cooking Channel",
    "Logo(LOGO).us": "Logo",
    "AdultSwim(ADSM).ca": "Adult Swim",
    "ANTENNA(KGBTDT).us": "ANTENNA",
    "CHARGE!(CHARGE).us": "CHARGE!",
    "FS1.us": "FS1",
    "FS2.us": "FS2",
    "NFLNetwork(NFLNET).us": "NFL Network",
    "NHLNetwork(NHLNET).us": "NHL Network",
    "MLBNetwork(MLBN).us": "MLB Network",
    "NBATV(NBATV).us": "NBA TV",
    "CBSSportsNetwork(CBSSN).us": "CBS Sports",
    "Ovation(OVATION).us": "Ovation",
    "UPTV.us": "UPTV",
    "COZITV(COZITV).us": "COZI TV",
    "OutdoorChannel(OUTD).us": "Outdoor Channel",
    "ASPiRE(ASPRE).us": "ASPiRE",
    "HBO.us": "HBO",
    "HBO2(HBOHIT).us": "HBO2",
    "HBOComedy(HBOC).us": "HBO Comedy",
    "HBOSignature(HBODRAM).us": "HBO Signature",
    "HBOWest(HBOHDP).us": "HBO West",
    "HBOZone(HBOMOV).us": "HBO Zone",
    "CinemaxHD(MAXHD).us": "Cinemax",
    "MoreMAX(MAXHIT).us": "MoreMAX",
    "ActionMAX(MAXACT).us": "ActionMAX",
    "5StarMAX(MAXCLAS).us": "5StarMAX",
    "Paramount+withShowtimeOnDemand(SHOWDM).us": "Showtime OnDemand",
    "ShowtimeExtreme(SHOWX).us": "Showtime Extreme",
    "ShowtimeNext(NEXT).us": "Showtime Next",
    "ShowtimeShowcase(SHOCSE).us": "Showtime Showcase",
    "ShowtimeFamilyzone(FAMZ).us": "Showtime Family",
    "ShowtimeWomen(WOMEN).us": "Showtime Women",
    "Starz(STARZ).us": "Starz",
    "StarzEdge(STZE).us": "Starz Edge",
    "StarzCinema(STZCI).us": "Starz Cinema",
    "StarzComedy(STZC).us": "Starz Comedy",
    "StarzEncore(STZENC).us": "Starz Encore",
    "StarzEncoreBlack(STZENBK).us": "Starz Encore Black",
    "StarzEncoreClassic(STZENCL).us": "Starz Encore Classic",
    "StarzEncoreFamily(STZENFM).us": "Starz Encore Family",
    "StarzEncoreWesterns(STZENWS).us": "Starz Encore Westerns",
    "StarzKids(STZK).us": "Starz Kids",
    "StarzEncoreAction(STZENAC).us": "Starz Encore Action",
    "ScreenPix(SCRNPIX).us": "ScreenPix",
    "ScreenPixAction(SCRNACT).us": "ScreenPix Action",
    "ScreenPixVoices(SCRNVOI).us": "ScreenPix Voices",
    "ScreenPixWesterns(SCRNWST).us": "ScreenPix Westerns",
    "MoviePlex(MPLEX).us": "MoviePlex",
    "MGM+Drive-In(MGMDRV).us": "MGM+ Drive-In",
    "MGM+HD(MGMHD).us": "MGM+",
    "MGM+Hits(MGMHIT).us": "MGM+ Hits",
    "SonyMovieChannel(SONY).us": "Sony Movies",
    "TheMovieChannel(TMC).us": "TMC",
}

# -------------------------------
# Utility functions
# -------------------------------

# Remove bracketed annotations and words like Live/New/Repeat anywhere
BRACKET_REMOVE_RE = re.compile(r"[\(\[\{].*?[\)\]\}]", flags=re.DOTALL)
LIVE_WORD_RE = re.compile(r"\b(Live|New|Repeat|Encore|Premiere)\b", flags=re.IGNORECASE)

def remove_brackets_and_markers(text: str) -> str:
    if not text:
        return ""
    t = BRACKET_REMOVE_RE.sub("", text)
    t = LIVE_WORD_RE.sub("", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t

# Detect sports by title/subtitle/desc keywords
SPORT_KEY_RE = re.compile(r"(NFL|MLB|NBA|NHL|NCAA|Soccer|Football|Baseball|Basketball|Hockey|MLS|WNBA|NASCAR|UFC|Boxing|Golf|Tennis|Rugby|Cricket)", re.IGNORECASE)

def looks_like_sports(*texts) -> bool:
    for t in texts:
        if not t:
            continue
        if SPORT_KEY_RE.search(t):
            return True
    return False

# Extract matchup using sub-title or description (preserve "at" if present, else "vs")
VS_RE = re.compile(r"(.+?)\s+(vs\.?|v\.?|at)\s+(.+)", re.IGNORECASE)
def extract_matchup(subtitle: str, desc: str, title: str) -> str:
    # Try subtitle first
    for src in (subtitle, desc, title):
        if not src:
            continue
        m = VS_RE.search(src)
        if m:
            left = m.group(1).strip()
            connector = m.group(2).lower()
            right = m.group(3).strip()
            # normalize connector: keep 'at' if 'at' used, else 'vs'
            connector_out = "at" if connector.startswith("at") else "vs"
            # produce "Team A at Team B" or "Team A vs Team B"
            return f"{left} {connector_out} {right}"
    # fallback: try to pick two capitalized name groups
    tokens = re.findall(r"[A-Z][\w&\.'\-\s]+", title or "")
    if len(tokens) >= 2:
        return f"{tokens[0].strip()} vs {tokens[1].strip()}"
    return remove_brackets_and_markers(title or "")

# Parse episode-num elements (onscreen / xmltv_ns / other)
def parse_episode_number(prog_elem: ET.Element):
    # Look for any episode-num elements
    for ep in prog_elem.findall("episode-num"):
        txt = (ep.text or "").strip()
        system = ep.attrib.get("system", "").lower()
        if not txt:
            continue
        # common onscreen format S01E09 or S1E9 or 1x09
        m = re.search(r"[sS]?0*?(\d+)[eE|xX|×]0*?(\d+)", txt)
        if m:
            season = int(m.group(1))
            episode = int(m.group(2))
            return f"S{season}E{episode}"
        # xmltv_ns: "0.8." or "1.8."
        if system == "xmltv_ns" or "." in txt:
            parts = [p for p in re.split(r"[.\-]", txt) if p != ""]
            if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
                # xmltv_ns is zero-based
                season = int(parts[0]) + 1
                episode = int(parts[1]) + 1
                return f"S{season}E{episode}"
        # onscreen might already be S01E09
        m2 = re.search(r"[sS](\d+)[^\d]*[eE](\d+)", txt)
        if m2:
            season = int(m2.group(1))
            episode = int(m2.group(2))
            return f"S{season}E{episode}"
    return None

# Format date (accept multiple input formats), return MM/DD/YYYY or None
def format_date_any(date_text: str, start_text: str=None) -> str:
    if not date_text and start_text:
        # try parse from start attribute e.g. "20250910120000 +0000" or "20250910"
        st = start_text.strip()
        # take leading digits (8 or 14)
        digits = re.match(r"(\d{8,14})", st)
        if digits:
            date_text = digits.group(1)
    if not date_text:
        return None
    s = date_text.strip()
    # possible formats to try
    fmts = ["%Y%m%d", "%Y-%m-%d", "%Y%m%d%H%M%S", "%Y-%m-%dT%H:%M:%S", "%Y"]
    for f in fmts:
        try:
            dt = datetime.strptime(s[: len(f.replace("%","").replace("Y","").replace("m","").replace("d","")) + 0], f) if False else None
        except Exception:
            dt = None
        # simpler: try parsing progressively with try/except
    # Real parsing attempts:
    for fmt in ("%Y%m%d%H%M%S", "%Y%m%d", "%Y-%m-%d", "%Y"):
        try:
            dt = datetime.strptime(s[: len(datetime.strftime(datetime.now(), fmt))], fmt) if False else datetime.strptime(s, fmt)
            return dt.strftime("%m/%d/%Y")
        except Exception:
            pass
    # try to extract 8-digit date anywhere
    m = re.search(r"(\d{4})[-]?(\d{2})[-]?(\d{2})", s)
    if m:
        try:
            dt = datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
            return dt.strftime("%m/%d/%Y")
        except Exception:
            pass
    # try start attribute first 8 digits
    if start_text:
        m2 = re.match(r"(\d{8})", start_text)
        if m2:
            s2 = m2.group(1)
            try:
                dt = datetime.strptime(s2, "%Y%m%d")
                return dt.strftime("%m/%d/%Y")
            except:
                pass
    return None

# Helper to keep only title+desc and remove other children (we use date/episode/subtitle before removing)
def keep_only_title_and_desc(prog: ET.Element):
    for child in list(prog):
        if child.tag not in ("title", "desc"):
            prog.remove(child)

# Sort key for programmes: by channel order then by start time (if present)
def programme_sort_key(prog, channel_order_map):
    channel = prog.attrib.get("channel", "")
    order = channel_order_map.get(channel, 9999)
    start = prog.attrib.get("start", "")
    # try parse start as datetime for correct sorting
    try:
        m = re.match(r"(\d{14})", start)
        if m:
            dt = datetime.strptime(m.group(1), "%Y%m%d%H%M%S")
            start_key = dt
        else:
            m2 = re.match(r"(\d{8})", start)
            if m2:
                start_key = datetime.strptime(m2.group(1), "%Y%m%d")
            else:
                start_key = start
    except Exception:
        start_key = start
    return (order, start_key)

# -------------------------------
# Core cleaning for a programme element
# -------------------------------
def build_clean_programme(prog: ET.Element):
    # find elements
    title_el = prog.find("title")
    subtitle_el = prog.find("sub-title") or prog.find("subtitle") or prog.find("sub_title")
    desc_el = prog.find("desc") or prog.find("description")
    episode_elems = prog.findall("episode-num")
    date_el = prog.find("date")

    raw_title = (title_el.text or "").strip() if title_el is not None and title_el.text else ""
    raw_sub = (subtitle_el.text or "").strip() if subtitle_el is not None and subtitle_el.text else ""
    raw_desc = (desc_el.text or "").strip() if desc_el is not None and desc_el.text else ""

    # detect sports (check title/sub/title/desc)
    sports_flag = looks_like_sports(raw_title) or looks_like_sports(raw_sub) or looks_like_sports(raw_desc)

    # extract matchup for sports
    matchup = None
    if sports_flag:
        matchup = extract_matchup(raw_sub, raw_desc, raw_title)

    # determine episode info (S#E#) if present
    episode_tag_value = None
    # prefer onscreen or xmltv_ns episode-num
    if episode_elems:
        # parse any found episode-num
        for ep in episode_elems:
            parsed = parse_episode_number(prog)
            if parsed:
                episode_tag_value = parsed
                break

    # determine date string (MM/DD/YYYY)
    date_str = None
    # try <date> element first
    if date_el is not None and date_el.text:
        date_str = format_date_any(date_el.text.strip(), prog.attrib.get("start", ""))
    else:
        date_str = format_date_any(None, prog.attrib.get("start", ""))

    # build new title and description text
    if sports_flag and matchup:
        new_title = matchup
        # description content: keep existing description as body; if empty, use matchup as body
        body = raw_desc if raw_desc else ""
        desc_text = f"{new_title}. {body}".strip()
    else:
        # not sports: clean the title to remove bracketed/markers
        new_title = remove_brackets_and_markers(raw_title)
        # decide if TV show (episode present) else movie
        if episode_tag_value:
            # ensure "S1E9" formatting without leading zeros
            # some parsed may be "S01E09" from earlier; normalize
            se_m = re.search(r"[sS]?0*?(\d+)[eE|xX|×]0*?(\d+)", episode_tag_value)
            if not se_m:
                # already S#E#
                m2 = re.search(r"[sS](\d+)[eE](\d+)", episode_tag_value)
                if m2:
                    season_n = int(m2.group(1))
                    episode_n = int(m2.group(2))
                else:
                    # fallback just use parsed value
                    season_episode = episode_tag_value
                    season_n = None
                    episode_n = None
            else:
                season_n = int(se_m.group(1))
                episode_n = int(se_m.group(2))
            # create S#E# format no leading zeros
            if season_n is not None and episode_n is not None:
                se_text = f"S{season_n}E{episode_n}"
            else:
                se_text = episode_tag_value  # fallback
            # description: "<Title> - S#E#. <desc>"
            body = raw_desc if raw_desc else ""
            desc_text = f"{new_title} - {se_text}. {body}".strip()
        else:
            # movie or no episode info
            body = raw_desc if raw_desc else ""
            desc_text = f"{new_title}. {body}".strip()

    # append date if available
    if date_str:
        desc_text = f"{desc_text} ({date_str})"

    # ensure title and desc elements exist in the programme element
    if title_el is None:
        title_el = ET.Element("title")
        prog.insert(0, title_el)
    title_el.text = new_title

    if desc_el is None:
        desc_el = ET.Element("desc")
        # place after title
        # remove existing children and append in order
        prog.append(desc_el)
    desc_el.text = desc_text

    # remove all other elements except title and desc
    keep_only_title_and_desc(prog)

# -------------------------------
# Main: read epg.xml -> write clean_epg.xml
# -------------------------------
def main():
    input_name = "epg.xml"
    output_name = "clean_epg.xml"

    # Safety checks
    if not os.path.exists(input_name):
        print(f"ERROR: Input file '{input_name}' not found in this folder. Place your original EPG file named '{input_name}' here and re-run.")
        return

    if os.path.abspath(input_name) == os.path.abspath(output_name):
        print("ERROR: Output filename would overwrite input. Aborting for safety.")
        return

    # Parse
    try:
        tree = ET.parse(input_name)
        root = tree.getroot()
    except Exception as e:
        print(f"ERROR: Failed to parse '{input_name}': {e}")
        return

    # Build order map
    channel_order = {cid: i for i, cid in enumerate(keep_channels)}

    # Collect kept channels and programmes
    kept_channels = []
    kept_programmes = []

    # iterate channels (do not remove from root while iterating)
    for ch in root.findall("channel"):
        cid = ch.attrib.get("id")
        if cid in keep_channels:
            # replace display-name(s) if mapping exists
            mapped = channel_display_map.get(cid)
            if mapped:
                # update all display-name tags (there could be multiple language versions)
                dns = ch.findall("display-name")
                if dns:
                    for dn in dns:
                        dn.text = mapped
                else:
                    # if no display-name exists, add one
                    dn = ET.Element("display-name")
                    dn.text = mapped
                    ch.insert(0, dn)
            kept_channels.append(ch)

    # iterate programmes
    for prog in root.findall("programme"):
        chan = prog.attrib.get("channel")
        if chan in keep_channels:
            # perform cleaning in place (we'll keep the element)
            try:
                build_clean_programme(prog)
                kept_programmes.append(prog)
            except Exception as e:
                # skip if some programme cannot be processed, but continue
                print(f"WARNING: Skipping programme due to error: {e}")
                continue

    # Sort channels by channel_order and keep the same element objects
    kept_channels.sort(key=lambda el: channel_order.get(el.attrib.get("id"), 9999))

    # Sort programmes by (channel order, start time)
    kept_programmes.sort(key=lambda p: programme_sort_key(p, channel_order))

    # Rebuild root: preserve root tag + attributes, but replace children
    new_root = ET.Element(root.tag, root.attrib)

    # Add channels then programmes
    for c in kept_channels:
        new_root.append(c)
    for p in kept_programmes:
        new_root.append(p)

    # Write out
    new_tree = ET.ElementTree(new_root)
    try:
        new_tree.write(output_name, encoding="utf-8", xml_declaration=True)
        print(f"✅ Done. Cleaned guide written to '{output_name}'.")
        print(f"Original file preserved as '{input_name}'.")
    except Exception as e:
        print(f"ERROR: Failed to write output file: {e}")

if __name__ == "__main__":
    main()
