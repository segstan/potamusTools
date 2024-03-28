
sgPluginExtension = {'Linux': '.so', 'Windows': '.mll', 'Darwin': '.bundle'}

sgDicAllLightTextures ={
    'PxrDomeLight': [
        "lightColorMap"
    ],
    'PxrDistantLight' : [],
    'PxrSphereLight' : [],
    'PxrRectLight': [
        "lightColorMap"
    ],
    'PxrCookieLightFilter': [
        "map"
    ],
    'PxrGoboLightFilter': [
        "map"
    ]
}

list3dFormat = ["abc","fbx","obj"]
listTextureFileExtension = ["jpg","tif","exr","png","hdr"]
listRendermanLights = ['PxrEnvDayLight','PxrMeshLight','PxrSphereLight',"PxrDomeLight","PxrRectLight","PxrDistantLight","PxrDiskLight","PxrCylinderLight","PxrPortalLight","PxrAovLight"]
listRendermanBlockers = ["PxrBarnLightFilter","PxrBlockerLightFilter","PxrCookieLightFilter","PxrGoboLightFilter","PxrIntMultLightFilter","PxrRampLightFilter","PxrRodLightFilter"]
listArnoldLights = ['aiSkyDomeLight','aiAreaLight','aiPhotometricLight',"aiLightPortal","ambientLight","directionalLight","pointLight","spotLight","areaLight","volumeLight","aiPhysicalSky"]

# Megascans find most accurate shader 
listTagsPlants= ["aquatic","plant","grass","herb","mushroom","ocean","shrub","succulent","tree","weed","wood","moss"]
listTagsRocks= ["rock","stone","ground","structure","brick","antique","building","cardboard","castle","manmade","modular","sandy","street","terrain","tiles","wall"]
listTagsMetals = ["metal","hardware","grass","herb","mushroom","ocean","shrub","succulent","tree","weed","wood","moss"]

# Key = maya, Value = Houdini
sgDicConvertLightNameParameter={
    'maya-houdini':{
        'color':'lightColor',
        'colorR':'lightColorr',
        'colorG':'lightColorg',
        'colorB':'lightColorb',
        'lightColor':'lightColor',
        'lightColorR':'lightColorr',
        'lightColorG':'lightColorg',
        'lightColorB':'lightColorb',
        'shadowColor':'shadowColor',
        'shadowColorR':'shadowColorr',
        'shadowColorG':'shadowColorg',
        'shadowColorB':'shadowColorb',
        'emissionFocusTint': 'emissionFocusTint',
        'emissionFocusTintR': 'emissionFocusTintr',
        'emissionFocusTintG': 'emissionFocusTintg',
        'emissionFocusTintB': 'emissionFocusTintb',
        'msApproxBleedR':'msApproxBleedr',
        'msApproxBleedG':'msApproxBleedg',
        'msApproxBleedB':'msApproxBleedb',
        'msApproxContributionR':'msApproxContributionr',
        'msApproxContributionG':'msApproxContributiong',
        'msApproxContributionB':'msApproxContributionb',
        'Position':'pos',
        'Value':'value',
        'Interp':'interp',
        'primaryVisibility': 'ri_visiblecamera',
        'visibleInRefractionPath':'ri_visibletransmission',
        },
	'houdini-houdini':{
		},
	'maya-maya':{
		},
    'houdini-katana':{
        'ri_visiblecamera':'prmanStatements.attributes.visibility.camera',
        'ri_visibletransmission': 'prmanStatements.attributes.visibility.transmission',
        'ri_indirect': 'prmanStatements.attributes.visibility.indirect',
        'lightColorr':'lightColor.$$.i0',
        'lightColorg':'lightColor.$$.i1',
        'lightColorb':'lightColor.$$.i2',
        'msApproxContributionr': "msApproxContribution.$$.i0",
        'msApproxContributiong': "msApproxContribution.$$.i1",
        'msApproxContributionb': "msApproxContribution.$$.i2",
        'msApproxBleedr':'msApproxBleed.$$.i0',
        'msApproxBleedg':'msApproxBleed.$$.i1',
        'msApproxBleedb':'msApproxBleed.$$.i2',
        'light_colorr':'lightColor.$$.i0',
        'light_colorg':'lightColor.$$.i1',
        'light_colorb':'lightColor.$$.i2',
        'shadowColorr':'shadowColor.$$.i0',
        'shadowColorg':'shadowColor.$$.i1',
        'shadowColorb':'shadowColor.$$.i2',
        'emissionFocusTintr':'emissionFocusTint.$$.i0',
        'emissionFocusTintg':'emissionFocusTint.$$.i1',
        'emissionFocusTintb':'emissionFocusTint.$$.i2',
		},
    'maya-katana':{
        'primaryVisibility': 'prmanStatements.attributes.visibility.camera',
        'visibleInRefractionPath': 'prmanStatements.attributes.visibility.transmission',
        'indirectBounce': 'prmanStatements.attributes.visibility.indirect',
		},
    'houdini-maya':{
        'lightColor':'color',
        'lightColorr':'colorR',
        'lightColorg':'colorG',
        'lightColorb':'colorB',
        'lightColor':'lightColor',
        'lightColorr':'lightColorR',
        'lightColorg':'lightColorG',
        'lightColorb':'lightColorB',
        'shadowColor':'shadowColor',
        'shadowColorr':'shadowColorR',
        'shadowColorg':'shadowColorG',
        'shadowColorb':'shadowColorB',
        'emissionFocusTint':'emissionFocusTint',
        'emissionFocusTintr':'emissionFocusTintR',
        'emissionFocusTintg':'emissionFocusTintG',
        'emissionFocusTintb':'emissionFocusTintB',
        'msApproxBleedr':'msApproxBleedR',
        'msApproxBleedg':'msApproxBleedG',
        'msApproxBleedb':'msApproxBleedB',
        'msApproxContributionr':'msApproxContributionR',
        'msApproxContributiong':'msApproxContributionG',
        'msApproxContributionb':'msApproxContributionB',
        'pos':'Position',
        'value':"Value",
        'interp':'Interp',
        'ri_visiblecamera':'primaryVisibility',
        'ogl_enablelight':'visibility',
        'ri_visibletransmission': 'visibleInRefractionPath',
		},
    'katana-maya':{
		},
    'katana-houdini':{
		'lightColor':[
            'lightColorr',
            'lightColorg',
            'lightColorb'
        ],
        'shadowColor':[ 
            'shadowColorr',
            'shadowColorg',
            'shadowColorb',
        ],
        'emissionFocusTint': [
            'emissionFocusTintr',
            'emissionFocusTintg',
            'emissionFocusTintb',
        ],
        'msApproxBleed':[
            'msApproxBleedr',
            'msApproxBleedg',
            'msApproxBleedb',
        ],
        'msApproxContribution':[
            'msApproxContributionr',
            'msApproxContributiong',
            'msApproxContributionb',
        ],
        },
}

sgListConnectionParms = ['shop_lightfilterpaths']


