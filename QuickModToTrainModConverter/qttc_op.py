import os
import bpy
import random
from bpy.types import Operator

class QTTC_OT_Convert(Operator):
    bl_idname = "qttc.convert"
    bl_label = "Convert"
    bl_description = "Convert QuickMod To TrainMod"

    directory: bpy.props.StringProperty(name="Directory", subtype='DIR_PATH')

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, convert):
        bodypath = os.path.join(self.directory, "quickMod_model_body.obj")
        bodyindices = []
        bodyindex = 0
        for i in range(0, 6):
            if os.path.exists(bodypath):
                bodyindices.append(bodyindex)
            bodyindex += 1
            bodypath = os.path.join(self.directory, f"quickMod_model_body{bodyindex}.obj")
        
        wheelpath = os.path.join(self.directory, "quickMod_model_wheels_extra1.obj")
        wheelindices = []
        wheelindex = 1
        while os.path.exists(bodypath):
            wheelindices.append(wheelindex)
            wheelindex += 1
            wheelpath = os.path.join(self.directory, f"quickMod_model_wheels_extra{bodyindex}.obj")
        
        texturepath = "quickMod_texture.png"
        texturemap = {}
        textureindex = 0
        for i in range(0, 6):
            texturemap[textureindex] = texturepath if os.path.exists(os.path.join(self.directory, texturepath)) \
                else "quickMod_texture.png"
            textureindex += 1
            texturepath = f"quickMod_texture{bodyindex}.png"

        modtext = open(os.path.join(self.directory, "mod.txt"), 'r')
        modname = "a"
        modlength = "1"
        modacc = "1"
        moddec = "1"
        modlocomotive = "false"
        modcontrol = "false"
        modcontroloffsets = ["0", "0", "0"]
        modsound = "none"
        modhorn = "diesel_dx"
        modpreset = "none"
        modpresetoffset = "0"
        modpresetaltoffset = "0"
        modpresetparent = "0"
        modpresetaltparent = "1"
        modcoupleroffset = "0.07000000029802323"
        modwheeloffsets = {}
        modpivotparent = "0"
        modpivotoffset = "0"
        modmaterials = {}

        for i in wheelindices:
            modwheeloffsets[i] = 0
        for i in bodyindices:
            modmaterials[i] = 'normal'

        modlines = modtext.readlines()
        for l in modlines:
            if l.startswith('name '):
                modname = l.removeprefix('name ').removesuffix('\n')
            elif l.startswith('length '):
                modlength = l.removeprefix('length ').removesuffix('\n')
            elif l.startswith('locomotive '):
                modlocomotive = l.removeprefix('locomotive ').removesuffix('\n')
            elif l.startswith('spawnControls '):
                modcontrol = l.removeprefix('spawnControls ').removesuffix('\n')
            elif l.startswith('driverSpawnOffset '):
                modcontroloffsets = l.removeprefix('driverSpawnOffset ').removesuffix('\n').split('_')
            elif l.startswith('soundPreset '):
                modsound = l.removeprefix('soundPreset ').removesuffix('\n')
            elif l.startswith('hornPreset '):
                modhorn = l.removeprefix('hornPreset ').removesuffix('\n')
            elif l.startswith('preset '):
                modpreset = l.removeprefix('preset ').removesuffix('\n')
            elif l.startswith('wheelPresetOffset '):
                modpresetoffset = l.removeprefix('wheelPresetOffset ').removesuffix('\n')
            elif l.startswith('wheelPresetAltOffset '):
                modpresetaltoffset = l.removeprefix('wheelPresetAltOffset ').removesuffix('\n')
            elif l.startswith('wheelPresetParentIndex '):
                modpresetparent = l.removeprefix('wheelPresetParentIndex ').removesuffix('\n')
            elif l.startswith('wheelPresetAltParentIndex '):
                modpresetaltparent = l.removeprefix('wheelPresetAltParentIndex ').removesuffix('\n')
            elif l.startswith('couplerOffset '):
                modcoupleroffset = l.removeprefix('couplerOffset ').removesuffix('\n')
            elif l.startswith('wheelOffset'):
                t = l.removeprefix('wheeloffset').removesuffix('\n').split()
                modwheeloffsets[int(t[0])] = t[1]
            elif l.startswith('pivotParentIndex '):
                modpivotparent = l.removeprefix('pivotParentIndex ').removesuffix('\n')
            elif l.startswith('pivotoffset '):
                modpivotoffset = l.removeprefix('pivotParentIndex ').removesuffix('\n')
            elif l.startswith('material'):
                t = l.removeprefix('material').removesuffix('\n').split()
                if len(t) == 1:
                    modmaterials[0] = int(t[0])
                else:
                    modmaterials[int(t[0])] = t[1]
        modtext.close()

        soundmap = {
            'none' : 'engine_mute',
            'diesel' : 'engine_diesel',
            'steam' : 'engine_steam',
            'electric' : 'engine_electric',
            'englishElectric' : 'engine_englishElectric'
        }
        hornmap = {
            'diesel_dx' : 'hornPreset_horn_dx',
            'diesel_dsj' : 'hornPreset_horn_dsj',
            'diesel_f7' : 'hornPreset_horn_f7',
            'diesel_nr' : 'hornPreset_horn_nr',
            'diesel_2tone1' : 'hornPreset_horn_twoTone_1',
            'diesel_2tone2' : 'hornPreset_horn_twoTone_2',
            'steam_flyer' : 'hornPreset_whistle_flyer',
            'steam_bigboy' : 'hornPreset_whistle_bigboy',
            'steam_berkshire' : 'hornPreset_whistle_berkshire',
            'steam_nyc6chime' : 'hornPreset_whistle_6chime',
            'ghost_horn1' : 'hornPreset_horn_u20c',
            'ghost_horn2' : 'hornPreset_horn_u20c',
            'ghost_whistle1' : 'hornPreset_whistle_1chime',
            'ghost_whistle2' : 'hornPreset_whistle_3chime',
            'electric_v8' : 'hornPreset_horn_v8',
            'diesel_u20c' : 'hornPreset_horn_u20c',
            'diesel_dg' : 'hornPreset_horn_dg',
            'diesel_da' : 'hornPreset_horn_da',
            'steam_ka' : 'hornPreset_whistle_ka',
            'steam_sunkenBerk' : 'hornPreset_whistle_sunkenBerk',
            'steam_rotary' : 'hornPreset_whistle_1chime',
            'steam_jgr' : 'hornPreset_whistle_jgr'
        }
        presetmap = {
            'none' : 'None',
            'steam_6' : 'wheelPreset_steam_6_flyer',
            'steam_6_6' : ('wheelPreset_steam_6_flyer'),
            'steam_8' : 'wheelPreset_steam_8_bigBoy',
            'steam_8_8' : ('wheelPreset_steam_8_bigBoy'),
            'steam_berkshire_8' : 'wheelPreset_steam_8_berkshire',
            'steam_berkshire_8_8' : ('wheelPreset_steam_8_berkshire'),
            'steam_2_4' : 'wheelPreset_steam_4-2_jgr',
            'steam_4' : 'wheelPreset_steam_4-0_jgr',
        }
        materialmap = {
            'normal' : 0,
            'alpha' : 1,
            'alphaCutout' : 4,
            'unlit' : 2,
            'alphaUnlit' : 3,
        }

        keaid = random.randint(10000,99999)
        keapath = os.path.join(self.directory, 'wagon.kea')
        keatext = open(keapath, 'w')
        keatext.write(f'''{{
    "dataVersion": 1,
    "rawName": "{modname}_{keaid}",
    "displayName": "{modname}",
    "description": "",
    "groups": [
    "   default"
    ],
    "dataType": 1,
    "id": "{keaid}",
    "duplicationPermission": 2,
    "variantPermission": 2,
    "variant": false,
    "variantName": "",
    "thumbnailRef": {{
        "assetName": "None",
        "variantOriginalAssetName": "None",
        "useVariantOriginalAsset": false
    }},
    "addonPrefabs": [],
    "tagData": {{
        "categoryTags": [
            "Locomotive"
        ],
        "regionTags": [
            "Global"
        ],
        "customTags": []
    }},
    "physicsData": {{
        "useCollision": false
    }},
    "equipData": {{
        "equipOffset": {{
            "x": 0.0,
            "y": 0.0,
            "z": 0.0
        }}
    }},
    "model": {{
        "masterMaterial": {{
            "m_FileID": 0,
            "m_PathID": 0
        }},
        "body": {{
            "meshes": [''')

        for i in bodyindices:
            keatext.write(f'''
				{{
					"name": "{i}",
					"mesh": {{
						"m_FileID": 0,
						"m_PathID": 0
					}},
					"meshRef": {{
						"assetName": "quickMod_model_body{i if i != 0 else ""}.obj",
						"variantOriginalAssetName": "None",
						"useVariantOriginalAsset": false
					}},
					"materialType": {materialmap[modmaterials[i]]},
					"material": {{
						"m_FileID": 0,
						"m_PathID": 0
					}},
					"castShadows": true,
					"texture": {{
						"m_FileID": 0,
						"m_PathID": 0
					}},
					"textureRef": {{
						"assetName": "{texturemap[i]}",
						"variantOriginalAssetName": "None",
						"useVariantOriginalAsset": false
					}},
					"colorCode": {{
						"m_FileID": 0,
						"m_PathID": 0
					}},
					"colorCodeRef": {{
						"colorCodeRaw": ""
					}},
					"paintable": false,
					"animation": {{
						"clipIndex": 0,
						"wrapMode": 2,
						"playSpeed": 1.0
					}},
					"useLegacyModelInvert": false
				}}{"" if i == bodyindices[-1] else ","}''')
        

        keatext.write(f'''
            ],
			"trackTexturePaintable": false
		}},
		"wheelData": [
			{{
				"detailName": "Back wheels",
				"usePreset": false,
				"modPresetName": "wheelPreset_freight_default",
				"preset": {{
					"m_FileID": 0,
					"m_PathID": 0
				}},
				"presetTextureOverride": {{
					"assetName": "None",
					"variantOriginalAssetName": "None",
					"useVariantOriginalAsset": false
				}},
				"materialOverride": {{
					"m_FileID": 0,
					"m_PathID": 0
				}},
				"customModel": {{
					"meshes": [
						{{
							"name": "Main",
							"mesh": {{
								"m_FileID": 0,
								"m_PathID": 0
							}},
							"meshRef": {{
								"assetName": "quickMod_model_wheels_back.obj",
								"variantOriginalAssetName": "None",
								"useVariantOriginalAsset": false
							}},
							"materialType": 0,
							"material": {{
								"m_FileID": 0,
								"m_PathID": 0
							}},
							"castShadows": true,
							"texture": {{
								"m_FileID": 0,
								"m_PathID": 0
							}},
							"textureRef": {{
								"assetName": "quickMod_texture.png",
								"variantOriginalAssetName": "None",
								"useVariantOriginalAsset": false
							}},
							"colorCode": {{
								"m_FileID": 0,
								"m_PathID": 0
							}},
							"colorCodeRef": {{
								"colorCodeRaw": ""
							}},
							"paintable": false,
							"animation": {{
								"clipIndex": 0,
								"wrapMode": 2,
								"playSpeed": 1.0
							}},
							"useLegacyModelInvert": false
						}}
					],
					"trackTexturePaintable": false
				}},
				"modelPosOffset": {{
					"x": 0.0,
					"y": 0.0,
					"z": 0.0
				}},
				"wheelPosition": 0,
				"customLength": 2.0,
				"flipModel": false,
				"lockToWagonBody": false
			}},
			{{
				"detailName": "Front wheels",
				"usePreset": false,
				"modPresetName": "wheelPreset_freight_default",
				"preset": {{
					"m_FileID": 0,
					"m_PathID": 0
				}},
				"presetTextureOverride": {{
					"assetName": "None",
					"variantOriginalAssetName": "None",
					"useVariantOriginalAsset": false
				}},
				"materialOverride": {{
					"m_FileID": 0,
					"m_PathID": 0
				}},
				"customModel": {{
					"meshes": [
						{{
							"name": "Main",
							"mesh": {{
								"m_FileID": 0,
								"m_PathID": 0
							}},
							"meshRef": {{
								"assetName": "quickMod_model_wheels_front.obj",
								"variantOriginalAssetName": "None",
								"useVariantOriginalAsset": false
							}},
							"materialType": 0,
							"material": {{
								"m_FileID": 0,
								"m_PathID": 0
							}},
							"castShadows": true,
							"texture": {{
								"m_FileID": 0,
								"m_PathID": 0
							}},
							"textureRef": {{
								"assetName": "quickMod_texture.png",
								"variantOriginalAssetName": "None",
								"useVariantOriginalAsset": false
							}},
							"colorCode": {{
								"m_FileID": 0,
								"m_PathID": 0
							}},
							"colorCodeRef": {{
								"colorCodeRaw": ""
							}},
							"paintable": false,
							"animation": {{
								"clipIndex": 0,
								"wrapMode": 2,
								"playSpeed": 1.0
							}},
							"useLegacyModelInvert": false
						}}
					],
					"trackTexturePaintable": false
				}},
				"modelPosOffset": {{
					"x": 0.0,
					"y": 0.0,
					"z": 0.0
				}},
				"wheelPosition": 1,
				"customLength": 2.0,
				"flipModel": false,
				"lockToWagonBody": false
			}}''')
        
        for i in wheelindices:
            keatext.write(f''',
			{{
				"detailName": "{i}",
				"usePreset": false,
				"modPresetName": "wheelPreset_freight_default",
				"preset": {{
					"m_FileID": 0,
					"m_PathID": 0
				}},
				"presetTextureOverride": {{
					"assetName": "None",
					"variantOriginalAssetName": "None",
					"useVariantOriginalAsset": false
				}},
				"materialOverride": {{
					"m_FileID": 0,
					"m_PathID": 0
				}},
				"customModel": {{
					"meshes": [
						{{
							"name": "Main",
							"mesh": {{
								"m_FileID": 0,
								"m_PathID": 0
							}},
							"meshRef": {{
								"assetName": "quickMod_model_wheels_extra{i}.obj",
								"variantOriginalAssetName": "None",
								"useVariantOriginalAsset": false
							}},
							"materialType": 0,
							"material": {{
								"m_FileID": 0,
								"m_PathID": 0
							}},
							"castShadows": true,
							"texture": {{
								"m_FileID": 0,
								"m_PathID": 0
							}},
							"textureRef": {{
								"assetName": "quickMod_texture.png",
								"variantOriginalAssetName": "None",
								"useVariantOriginalAsset": false
							}},
							"colorCode": {{
								"m_FileID": 0,
								"m_PathID": 0
							}},
							"colorCodeRef": {{
								"colorCodeRaw": ""
							}},
							"paintable": false,
							"animation": {{
								"clipIndex": 0,
								"wrapMode": 2,
								"playSpeed": 1.0
							}},
							"useLegacyModelInvert": false
						}}
					],
					"trackTexturePaintable": false
				}},
				"modelPosOffset": {{
					"x": 0.0,
					"y": 0.0,
					"z": 0.0
				}},
				"wheelPosition": 2,
				"customLength": {modwheeloffsets[i]},
				"flipModel": false,
				"lockToWagonBody": {"true" if modpivotparent == str(i) else "false"}
			}}''')
        
        keatext.write(fr'''
		],
		"couplerData": [
			{{
				"detailName": "Back coupler",
				"usePreset": false,
				"modPresetName": "couplerPreset_default",
				"preset": {{
					"m_FileID": 0,
					"m_PathID": 0
				}},
				"presetTextureOverride": {{
					"assetName": "None",
					"variantOriginalAssetName": "None",
					"useVariantOriginalAsset": false
				}},
				"materialOverride": {{
					"m_FileID": 0,
					"m_PathID": 0
				}},
				"customModel": {{
					"meshes": [
                        {{
							"name": "Main",
							"mesh": {{
								"m_FileID": 0,
								"m_PathID": 0
							}},
							"meshRef": {{
								"assetName": "quickMod_model_couple_back.obj",
								"variantOriginalAssetName": "None",
								"useVariantOriginalAsset": false
							}},
							"materialType": 0,
							"material": {{
								"m_FileID": 0,
								"m_PathID": 0
							}},
							"castShadows": true,
							"texture": {{
								"m_FileID": 0,
								"m_PathID": 0
							}},
							"textureRef": {{
								"assetName": "quickMod_texture.png",
								"variantOriginalAssetName": "None",
								"useVariantOriginalAsset": false
							}},
							"colorCode": {{
								"m_FileID": 0,
								"m_PathID": 0
							}},
							"colorCodeRef": {{
								"colorCodeRaw": ""
							}},
							"paintable": false,
							"animation": {{
								"clipIndex": 0,
								"wrapMode": 2,
								"playSpeed": 1.0
							}},
							"useLegacyModelInvert": false
						}}
                    ],
					"trackTexturePaintable": false
				}},
				"modelPosOffset": {{
					"x": 0.0,
					"y": 0.0,
					"z": 0.0
				}},
				"useCustomOffset": true,
				"couplerOffset": {modcoupleroffset}
			}},
			{{
				"detailName": "Front coupler",
				"usePreset": false,
				"modPresetName": "couplerPreset_default",
				"preset": {{
					"m_FileID": 0,
					"m_PathID": 0
				}},
				"presetTextureOverride": {{
					"assetName": "None",
					"variantOriginalAssetName": "None",
					"useVariantOriginalAsset": false
				}},
				"materialOverride": {{
					"m_FileID": 0,
					"m_PathID": 0
				}},
				"customModel": {{
					"meshes": [
                        {{
							"name": "Main",
							"mesh": {{
								"m_FileID": 0,
								"m_PathID": 0
							}},
							"meshRef": {{
								"assetName": "quickMod_model_couple_front.obj",
								"variantOriginalAssetName": "None",
								"useVariantOriginalAsset": false
							}},
							"materialType": 0,
							"material": {{
								"m_FileID": 0,
								"m_PathID": 0
							}},
							"castShadows": true,
							"texture": {{
								"m_FileID": 0,
								"m_PathID": 0
							}},
							"textureRef": {{
								"assetName": "quickMod_texture.png",
								"variantOriginalAssetName": "None",
								"useVariantOriginalAsset": false
							}},
							"colorCode": {{
								"m_FileID": 0,
								"m_PathID": 0
							}},
							"colorCodeRef": {{
								"colorCodeRaw": ""
							}},
							"paintable": false,
							"animation": {{
								"clipIndex": 0,
								"wrapMode": 2,
								"playSpeed": 1.0
							}},
							"useLegacyModelInvert": false
						}}
                    ],
					"trackTexturePaintable": false
				}},
				"modelPosOffset": {{
					"x": 0.0,
					"y": 0.0,
					"z": 0.0
				}},
				"useCustomOffset": true,
				"couplerOffset": {modcoupleroffset}
			}}
		],
		"lowDetailMeshes": [],
		"lights": [],
		"randomizer": {{
			"useMaterialOnWheels": false,
			"modelIndexesToRandomize": [],
			"randomTexures": [],
			"randomMeshes": [],
			"chanceToHideRandomizedMesh": 0
		}}
	}},
	"values": {{
		"locomotive": {modlocomotive},
		"length": {modlength},
		"speedAcc": {modacc},
		"speedDec": {moddec},
		"overrideCollision": false,
		"useDynamicUVsForLivery": true,
		"useLiveryOnWheels": true,
		"useLiveryOnlyOnFirstMesh": false,
		"pivotStyle": {"0" if len(wheelindices) == 0 else "1"}
	}},
	"audio": {{
		"modAudioPresetName": "{soundmap[modsound]}",
		"enginePreset": {{
			"m_FileID": 0,
			"m_PathID": 0
		}},
		"engineAudioRef_Start": {{
			"assetName": "None",
			"variantOriginalAssetName": "None",
			"useVariantOriginalAsset": false
		}},
		"engineAudioRef_Stop": {{
			"assetName": "None",
			"variantOriginalAssetName": "None",
			"useVariantOriginalAsset": false
		}},
		"engineAudioRef_ColdStart": {{
			"assetName": "None",
			"variantOriginalAssetName": "None",
			"useVariantOriginalAsset": false
		}},
		"engineAudioRef_Shutdown": {{
			"assetName": "None",
			"variantOriginalAssetName": "None",
			"useVariantOriginalAsset": false
		}},
		"engineAudioRef_LoopIdle": {{
			"assetName": "None",
			"variantOriginalAssetName": "None",
			"useVariantOriginalAsset": false
		}},
		"engineAudioRef_LoopEngine1": {{
			"assetName": "None",
			"variantOriginalAssetName": "None",
			"useVariantOriginalAsset": false
		}},
		"engineAudioRef_LoopEngine2": {{
			"assetName": "None",
			"variantOriginalAssetName": "None",
			"useVariantOriginalAsset": false
		}},
		"engineAudioRef_LoopEngine3": {{
			"assetName": "None",
			"variantOriginalAssetName": "None",
			"useVariantOriginalAsset": false
		}},
		"engineAudioRef_LoopEngine4": {{
			"assetName": "None",
			"variantOriginalAssetName": "None",
			"useVariantOriginalAsset": false
		}},
		"hornAssetType": 0,
		"modHornPresetName": "hornmap[modhorn]",
		"hornPreset": {{
			"m_FileID": 0,
			"m_PathID": 0
		}},
		"hornAudioRef": {{
			"assetName": "None",
			"variantOriginalAssetName": "None",
			"useVariantOriginalAsset": false
		}},
		"hornStepAudioRef_Start": {{
			"assetName": "None",
			"variantOriginalAssetName": "None",
			"useVariantOriginalAsset": false
		}},
		"hornStepAudioRef_Loop": {{
			"assetName": "None",
			"variantOriginalAssetName": "None",
			"useVariantOriginalAsset": false
		}},
		"hornStepAudioRef_Stop": {{
			"assetName": "None",
			"variantOriginalAssetName": "None",
			"useVariantOriginalAsset": false
		}},
		"whistleSteamLength": 1.0,
		"useTrackClicks": false,
		"muteAudio": false
	}},
	"cab": {{
		"useCabPreset": true,
		"modCabPresetName": "cabPreset_diesel",
		"cabOffset": {{
			"x": {modcontroloffsets[0]},
			"y": {modcontroloffsets[1]},
			"z": {modcontroloffsets[2]}
		}},
		"spawnOffset": {{
			"x": 0.0,
			"y": 0.0,
			"z": 0.0
		}},
		"hornOffset": {{
			"x": 0.0,
			"y": 0.0,
			"z": 0.0
		}}
	}},
	"effects": {{
		"particleEffects": [],
		"lightEffects": []
	}},
	"addons": {{
		"plowData": {{
			"basePosition": {{
				"x": 0.0,
				"y": 0.0,
				"z": 0.0
			}},
			"baseScale": 0.0,
			"flipModel": false
		}},
		"pantographData": {{
			"basePosition": {{
				"x": 0.0,
				"y": 0.0,
				"z": 0.0
			}},
			"baseScale": 0.0,
			"flipModel": false
		}},
		"pantographAltData": {{
			"basePosition": {{
				"x": 0.0,
				"y": 0.0,
				"z": 0.0
			}},
			"baseScale": 0.0,
			"flipModel": false
		}},
		"useAltPantograph": false
	}}
}}''')

        keatext.close()

        return {'FINISHED'}