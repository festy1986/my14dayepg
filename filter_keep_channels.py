import xml.etree.ElementTree as ET
import re
from datetime import datetime

# === Keep channels list ===
keep_channels = [
    "Comet(COMET).us : 'Comet'",
    "Laff(LAFF).us : 'Laff'",
    "ABC(WMTW).us : 'ABC'",
    "FOX(WFXT).us : 'FOX'",
    "FOX(WPFO).us : 'FOX'",
    "NBC(WBTSCD).us : 'NBC'",
    "NBC(WCSH).us : 'NBC'",
    "ABC(WCVB).us : 'ABC'",
    "ABC(WMTW).us : 'ABC'",
    "NewEnglandCableNews(NECN).us : 'NewEnglandCableNews'",
    "PBS(HD01).us : 'PBS'",
    "CW(WLVI).us : 'CW'",
    "CBS(WBZ).us : 'CBS'",
    "WSBK.us : 'WSBK'",
    "CBS(WGME).us : 'CBS'",
    "ION.us : 'ION'",
    "MeTVNetwork(METVN).us : 'MeTVNetwork'",
    "INSPHD(INSPHD).us : 'INSPHD'",
    "GameShowNetwork(GSN).us : 'GameShowNetwork'",
    "FamilyEntertainmentTelevision(FETV).us : 'FamilyEntertainmentTelevision'",
    "Heroes&IconsNetwork(HEROICN).us : 'Heroes&IconsNetwork'",
    "TurnerClassicMoviesHD(TCMHD).us : 'TurnerClassicMoviesHD'",
    "OprahWinfreyNetwork(OWN).us : 'OprahWinfreyNetwork'",
    "BET.us : 'BET'",
    "DiscoveryChannel(DSC).us : 'DiscoveryChannel'",
    "Freeform(FREEFRM).us : 'Freeform'",
    "USANetwork(USA).us : 'USANetwork'",
    "NewEnglandSportsNetwork(NESN).us : 'NewEnglandSportsNetwork'",
    "NewEnglandSportsNetworkPlus(NESNPL).us : 'NewEnglandSportsNetworkPlus'",
    "NBCSportsBoston(NBCSB).us : 'NBCSportsBoston'",
    "ESPN.us : 'ESPN'",
    "ESPN2.us : 'ESPN2'",
    "ESPNEWS.us : 'ESPNEWS'",
    "AWealthofEntertainmentHD(AWEHD).us : 'AWealthofEntertainmentHD'",
    "WEtv(WE).us : 'WEtv'",
    "OxygenTrueCrime(OXYGEN).us : 'OxygenTrueCrime'",
    "DisneyChannel(DISN).us : 'DisneyChannel'",
    "DisneyJunior(DJCH).us : 'DisneyJunior'",
    "DisneyXD(DXD).us : 'DisneyXD'",
    "CartoonNetwork(TOONLSH).us : 'CartoonNetwork'",
    "Nickelodeon(NIK).us : 'Nickelodeon'",
    "MSNBC.us : 'MSNBC'",
    "CableNewsNetwork(CNN).us : 'CableNewsNetwork'",
    "HLN.us : 'HLN'",
    "CNBC.us : 'CNBC'",
    "FoxNewsChannel(FNC).us : 'FoxNewsChannel'",
    "LifetimeRealWomen(LRW).us : 'LifetimeRealWomen'",
    "TNT.us : 'TNT'",
    "Lifetime(LIFE).us : 'Lifetime'",
    "LMN.us : 'LMN'",
    "TLC.us : 'TLC'",
    "AMC.us : 'AMC'",
    "Home&GardenTelevisionHD(HGTVD).us : 'Home&GardenTelevisionHD'",
    "TheTravelChannel(TRAV).us : 'TheTravelChannel'",
    "A&E(AETV).us : 'A&E'",
    "FoodNetwork(FOOD).us : 'FoodNetwork'",
    "Bravo(BRAVO).us : 'Bravo'",
    "truTV(TRUTV).us : 'truTV'",
    "NationalGeographicHD(NGCHD).us : 'NationalGeographicHD'",
    "HallmarkChannel(HALL).us : 'HallmarkChannel'",
    "HallmarkFamily(HFM).us : 'HallmarkFamily'",
    "HallmarkMystery(HMYS).us : 'HallmarkMystery'",
    "SYFY.us : 'SYFY'",
    "AnimalPlanet(APL).us : 'AnimalPlanet'",
    "History(HISTORY).us : 'History'",
    "TheWeatherChannel(WEATH).us : 'TheWeatherChannel'",
    "ParamountNetwork(PAR).us : 'ParamountNetwork'",
    "ComedyCentral(COMEDY).us : 'ComedyCentral'",
    "FXM.us : 'FXM'",
    "FXX.us : 'FXX'",
    "FX.us : 'FX'",
    "E!EntertainmentTelevisionHD(EHD).us : 'E!EntertainmentTelevisionHD'",
    "AXSTV(AXSTV).us : 'AXSTV'",
    "TVLand(TVLAND).us : 'TVLand'",
    "TBS.us : 'TBS'",
    "VH1.us : 'VH1'",
    "MTV-MusicTelevision(MTV).us : 'MTV-MusicTelevision'",
    "CMT(CMTV).us : 'CMT'",
    "DestinationAmerica(DEST).us : 'DestinationAmerica'",
    "MagnoliaNetwork(MAGN).us : 'MagnoliaNetwork'",
    "MagnoliaNetworkHD(Pacific)(MAGNPHD).us : 'MagnoliaNetworkHD(Pacific)'",
    "DiscoveryLifeChannel(DLC).us : 'DiscoveryLifeChannel'",
    "NationalGeographicWild(NGWILD).us : 'NationalGeographicWild'",
    "SmithsonianChannelHD(SMTSN).us : 'SmithsonianChannelHD'",
    "BBCAmerica(BBCA).us : 'BBCAmerica'",
    "POP(POPSD).us : 'POP'",
    "Crime&InvestigationNetworkHD(CINHD).us : 'Crime&InvestigationNetworkHD'",
    "Vice(VICE).us : 'Vice'",
    "InvestigationDiscoveryHD(IDHD).us : 'InvestigationDiscoveryHD'",
    "ReelzChannel(REELZ).us : 'ReelzChannel'",
    "DiscoveryFamilyChannel(DFC).us : 'DiscoveryFamilyChannel'",
    "Science(SCIENCE).us : 'Science'",
    "AmericanHeroesChannel(AHC).us : 'AmericanHeroesChannel'",
    "AMC+(AMCPLUS).us : 'AMC+'",
    "Fuse(FUSE).us : 'Fuse'",
    "MusicTelevisionHD(MTV2HD).us : 'MusicTelevisionHD'",
    "IFC.us : 'IFC'",
    "FYI(FYISD).us : 'FYI'",
    "CookingChannel(COOK).us : 'CookingChannel'",
    "Logo(LOGO).us : 'Logo'",
    "AdultSwim(ADSM).ca : 'AdultSwim'",
    "ANTENNA(KGBTDT).us : 'ANTENNA'",
    "CHARGE!(CHARGE).us : 'CHARGE!'",
    "FS1.us : 'FS1'",
    "FS2.us : 'FS2'",
    "NFLNetwork(NFLNET).us : 'NFLNetwork'",
    "NHLNetwork(NHLNET).us : 'NHLNetwork'",
    "MLBNetwork(MLBN).us : 'MLBNetwork'",
    "NBATV(NBATV).us : 'NBATV'",
    "CBSSportsNetwork(CBSSN).us : 'CBSSportsNetwork'",
    "Ovation(OVATION).us : 'Ovation'",
    "UPTV.us : 'UPTV'",
    "COZITV(COZITV).us : 'COZITV'",
    "OutdoorChannel(OUTD).us : 'OutdoorChannel'",
    "ASPiRE(ASPRE).us : 'ASPiRE'",
    "HBO.us : 'HBO'",
    "HBO2(HBOHIT).us : 'HBO2'",
    "HBOComedy(HBOC).us : 'HBOComedy'",
    "HBOSignature(HBODRAM).us : 'HBOSignature'",
    "HBOWest(HBOHDP).us : 'HBOWest'",
    "HBOZone(HBOMOV).us : 'HBOZone'",
    "CinemaxHD(MAXHD).us : 'CinemaxHD'",
    "MoreMAX(MAXHIT).us : 'MoreMAX'",
    "ActionMAX(MAXACT).us : 'ActionMAX'",
    "5StarMAX(MAXCLAS).us : '5StarMAX'",
    "Paramount+withShowtimeOnDemand(SHOWDM).us : 'Paramount+withShowtimeOnDemand'",
    "ShowtimeExtreme(SHOWX).us : 'ShowtimeExtreme'",
    "ShowtimeNext(NEXT).us : 'ShowtimeNext'",
    "ShowtimeShowcase(SHOCSE).us : 'ShowtimeShowcase'",
    "ShowtimeFamilyzone(FAMZ).us : 'ShowtimeFamilyzone'",
    "ShowtimeWomen(WOMEN).us : 'ShowtimeWomen'",
    "Starz(STARZ).us : 'Starz'",
    "StarzEdge(STZE).us : 'StarzEdge'",
    "StarzCinema(STZCI).us : 'StarzCinema'",
    "StarzComedy(STZC).us : 'StarzComedy'",
    "StarzEncore(STZENC).us : 'StarzEncore'",
    "StarzEncoreBlack(STZENBK).us : 'StarzEncoreBlack'",
    "StarzEncoreClassic(STZENCL).us : 'StarzEncoreClassic'",
    "StarzEncoreFamily(STZENFM).us : 'StarzEncoreFamily'",
    "StarzEncoreWesterns(STZENWS).us : 'StarzEncoreWesterns'",
    "StarzKids(STZK).us : 'StarzKids'",
    "StarzEncoreAction(STZENAC).us : 'StarzEncoreAction'",
    "ScreenPix(SCRNPIX).us : 'ScreenPix'",
    "ScreenPixAction(SCRNACT).us : 'ScreenPixAction'",
    "ScreenPixVoices(SCRNVOI).us : 'ScreenPixVoices'",
    "ScreenPixWesterns(SCRNWST).us : 'ScreenPixWesterns'",
    "MoviePlex(MPLEX).us : 'MoviePlex'",
    "MGM+Drive-In(MGMDRV).us : 'MGM+Drive-In'",
    "MGM+HD(MGMHD).us : 'MGM+HD'",
    "MGM+Hits(MGMHIT).us : 'MGM+Hits'",
    "SonyMovieChannel(SONY).us : 'SonyMovieChannel'",
    "TheMovieChannel(TMC).us : 'TheMovieChannel'"
]

channel_map = {}
for ch in keep_channels:
    match = re.match(r"(.+)\s*:\s*'(.+)'", ch)
    if match:
        channel_map[match.group(1).strip()] = match.group(2).strip()

input_file = "epg.xml"
output_file = "filtered_epg.xml"

tree = ET.parse(input_file)
root = tree.getroot()

# Clean and filter channels
for channel in root.findall("channel"):
    ch_id = channel.get("id")
    if ch_id in channel_map:
        display_name_elem = channel.find("display-name")
        if display_name_elem is not None:
            display_name_elem.text = channel_map[ch_id]
    else:
        root.remove(channel)

# Clean programmes
for programme in root.findall("programme"):
    ch_id = programme.get("channel")
    if ch_id not in channel_map:
        root.remove(programme)
        continue

    # Clean title
    title_elem = programme.find("title")
    if title_elem is not None:
        title_text = title_elem.text or ""
        # Remove "Live", "New", etc.
        title_text = re.sub(r"\b(Live|New)\b", "", title_text, flags=re.IGNORECASE).strip()

        # Detect sports and replace generic title with teams if available
        if any(sport in title_text for sport in ["MLB Baseball", "NBA Basketball", "NFL Football", "NHL Hockey"]):
            desc_elem = programme.find("desc")
            if desc_elem is not None and "-" in desc_elem.text:
                # Example: "Boston Red Sox - New York Yankees"
                teams = desc_elem.text.split("-")
                if len(teams) == 2:
                    title_text = f"{teams[0].strip()} vs {teams[1].strip()}"
        title_elem.text = title_text

    # Build description
    desc_elem = programme.find("desc")
    episode_elem = programme.find("episode-num")
    date_elem = programme.find("date")
    desc_text = ""

    if episode_elem is not None:
        desc_text += episode_elem.text + " - " if episode_elem.text else ""

    if desc_elem is not None:
        desc_text += desc_elem.text + " " if desc_elem.text else ""

    if date_elem is not None:
        try:
            # Try to parse as YYYYMMDD
            air_date = datetime.strptime(date_elem.text, "%Y%m%d")
            desc_text += f"({air_date.strftime('%m/%d/%Y')})"
        except:
            # Otherwise just keep original text
            desc_text += f"({date_elem.text})"

    # Replace description
    if desc_elem is not None:
        desc_elem.text = desc_text

# Write filtered XML
tree.write(output_file, encoding="utf-8")
print(f"Filtered EPG saved to {output_file}")
