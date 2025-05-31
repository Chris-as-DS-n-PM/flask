from flask import Flask, render_template

app = Flask(__name__)

CHANNELS = {
    "Nature": ["EarthPorn", "BotanicalPorn", "WaterPorn", "SeaPorn", "SkyPorn", "FirePorn", "DesertPorn", "WinterPorn", "AutumnPorn", "WeatherPorn", "GeologyPorn", "SpacePorn", "BeachPorn", "MushroomPorn", "SpringPorn", "SummerPorn", "LavaPorn", "LakePorn"],
    "Synthetic": ["CityPorn", "VillagePorn", "RuralPorn", "ArchitecturePorn", "HousePorn", "CabinPorn", "ChurchPorn", "AbandonedPorn", "CemeteryPorn", "InfrastructurePorn", "MachinePorn", "CarPorn", "F1Porn", "MotorcyclePorn", "MilitaryPorn", "GunPorn", "KnifePorn", "BoatPorn", "RidesPorn", "DestructionPorn", "ThingsCutInHalfPorn", "StarshipPorn", "ToolPorn", "TechnologyPorn", "BridgePorn", "PolicePorn", "SteamPorn", "RetailPorn", "SpaceFlightPorn", "roadporn", "drydockporn"],
    "Organic": ["AnimalPorn", "HumanPorn", "EarthlingPorn", "AdrenalinePorn", "ClimbingPorn", "SportsPorn", "AgriculturePorn", "TeaPorn", "BonsaiPorn", "FoodPorn", "CulinaryPorn", "DessertPorn"],
    "Aesthetic": ["DesignPorn", "RoomPorn", "AlbumArtPorn", "MetalPorn", "MoviePosterPorn", "TelevisionPosterPorn", "ComicBookPorn", "StreetArtPorn", "AdPorn", "ArtPorn", "FractalPorn", "InstrumentPorn", "ExposurePorn", "MacroPorn", "MicroPorn", "GeekPorn", "MTGPorn", "GamerPorn", "PowerWashingPorn", "AerialPorn", "OrganizationPorn", "FashionPorn", "AVPorn", "ApocalypsePorn", "InfraredPorn", "ViewPorn", "HellscapePorn", "sculptureporn"],
    "Scholastic": ["HistoryPorn", "UniformPorn", "BookPorn", "NewsPorn", "QuotesPorn", "FuturePorn", "FossilPorn", "MegalithPorn", "ArtefactPorn"]
}

@app.route('/')
def index():
    return render_template('index.html', categories=CHANNELS)

@app.route('/watch/<channelname>')
def watch(channelname):
    return render_template('watch.html', channel_name=channelname)

if __name__ == '__main__':
    app.run(debug=True)
