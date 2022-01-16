var g_objectColors = {
    "Arecibo Observatory":"#FDB813",
    "Haute-Provence Observatory":"#F4F1C9",
    "Roque de los Muchachos Observatory":"#F4F1C9",
    "Lick Observatory":"#F4F1C9",
    "Multiple Observatories":"#F4F1C9",
    "Fred Lawrence Whipple Observatory":"#F4F1C9",
    "W. M. Keck Observatory":"#F4F1C9",
    "La Silla Observatory":"#F4F1C9",
    "Anglo-Australian Telescope":"#F4F1C9",
    "OGLE":"#F4F1C9",
    "Hubble Space Telescope":"#0EC0A6",
    "Okayama Astrophysical Observatory":"#F4F1C9",
    "McDonald Observatory":"#F4F1C9",
    "TrES":"#F4F1C9",
    "Paranal Observatory":"#F4F1C9",
    "Thueringer Landessternwarte Tautenburg":"#F4F1C9",
    "Subaru Telescope":"#F4F1C9",
    "Oak Ridge Observatory":"#F4F1C9",
    "Kitt Peak National Observatory":"#F4F1C9",
    "XO":"#F4F1C9",
    "Palomar Observatory":"#F4F1C9",
    "Spitzer Space Telescope":"#F4F1C9",
    "HATNet":"#F4F1C9",
    "SuperWASP":"#F4F1C9",
    "Gemini Observatory":"#F4F1C9",
    "Xinglong Station":"#F4F1C9",
    "Teide Observatory":"#F4F1C9",
    "CoRoT":"#F4F1C9",
    "MOA":"#F4F1C9",
    "Las Campanas Observatory":"#F4F1C9",
    "MEarth Project":"#F4F1C9",
    "Bohyunsan Optical Astronomical Observatory":"#F4F1C9",
    "Yunnan Astronomical Observatory":"#F4F1C9",
    "Kepler":"#A7DEDA",
    "Infrared Survey Facility":"#F4F1C9",
    "Parkes Observatory":"#F4F1C9",
    "Qatar":"#F4F1C9",
    "Leoncito Astronomical Complex":"#F4F1C9",
    "KELT":"#F4F1C9",
    "United Kingdom Infrared Telescope":"#F4F1C9",
    "HATSouth":"#F4F1C9",
    "K2":"#F4F1C9",
    "Cerro Tololo Inter-American Observatory":"#F4F1C9",
    "Large Binocular Telescope Observatory":"#F4F1C9",
    "Multiple Facilities":"#F4F1C9",
    "KELT-South":"#F4F1C9",
    "KMTNet":"#F4F1C9",
    "SuperWASP-South":"#F4F1C9",
    "European Southern Observatory":"#F4F1C9",
    "SuperWASP-North":"#F4F1C9",
    "Apache Point Observatory":"#F4F1C9",
    "KELT-North":"#F4F1C9",
    "Transiting Exoplanet Survey Satellite (TESS)":"#F4F1C9",
    "Calar Alto Observatory":"#F4F1C9",
    "WASP-South":"#F4F1C9",
    "Mauna Kea Observatory":"#F4F1C9",
    "Acton Sky Portal Observatory":"#F4F1C9",
    "Atacama Large Millimeter Array (ALMA)":"#F4F1C9",
    "Haleakala Observatory":"#F4F1C9"
}



function g_objectStrokes (d) { 
    var objectStrokes = {
        "True":"#6b93d6",
        "False":"black"
    }
    return objectStrokes["true"] 
}

ggalaxy = draw_scatter(
    "ggalaxy",
    galaxies,
    g_objectColors,
    height,
    width
)