import torch
import safetensors
import safetensors.torch
import os
import copy

EMA_PREFIX = "model_ema."

METADATA = {'epoch': 0, 'global_step': 0, 'pytorch-lightning_version': '1.6.0'}

IDENTIFICATION = {
    "VAE": {
        "SD-v1": 0,
        "SD-v2": 869,
        "NAI": 2982,
        "WD-VAE-v1": 155,
        "WD-VAE-v2": 41
    },
    "CLIP-v1": {
        "SD-v1": 0,
    },
    "CLIP-v2": {
        "SD-v2": 1141,
        "WD-v1-4": 2543
    }
}

COMPONENTS = {
    "UNET-v1-SD": {
        "keys": {},
        "source": "UNET-v1-SD.txt",
        "prefix": "model.diffusion_model."
    },
    "UNET-v1-UP": {
        "keys": {},
        "source": "UNET-v1-UP.txt",
        "prefix": "model_ema.diffusion_model."
    },
    "UNET-v1-DOWN": {
        "keys": {},
        "source": "UNET-v1-DOWN.txt",
        "prefix": "model_ema.diffusion_model."
    },
    "UNET-v1-EMA": {
        "keys": {},
        "source": "UNET-v1-EMA.txt",
        "prefix": "model_ema.diffusion_model"
    },
    "UNET-v1-Inpainting": {
        "keys": {},
        "source": "UNET-v1-Inpainting.txt",
        "prefix": "model.diffusion_model."
    },
    "UNET-v1-Pix2Pix": {
        "keys": {},
        "source": "UNET-v1-Pix2Pix.txt",
        "prefix": "model.diffusion_model."
    },
    "UNET-v1-Pix2Pix-EMA": {
        "keys": {},
        "source": "UNET-v1-Pix2Pix-EMA.txt",
        "prefix": "model_ema.diffusion_model"
    },
#    "UNET-v1-SKIP": {
#        "keys": {},
#        "source": "UNET-v1-SKIP.txt",
#        "prefix": ""
#    },
#    "UNET-v1-EMBLAY": {
#        "keys": {},
#        "source": "UNET-v1-EMBLAY.txt",
#        "prefix": ""
#    },
#    "UNET-v1-TIME-EMB": {
#        "keys": {},
#        "source": "UNET-v1-TIME-EMB.txt",
#        "prefix": ""
#    },
#    "UNET-v1-MID": {
#        "keys": {},
#        "source": "UNET-v1L-MID.txt",
#        "prefix": ""
#    },
    "UNET-v2-SD": {
        "keys": {},
        "source": "UNET-v2-SD.txt",
        "prefix": "model.diffusion_model."
    },
    "UNET-v2-Inpainting": {
        "keys": {},
        "source": "UNET-v2-Inpainting.txt",
        "prefix": "model.diffusion_model."
    },
    "UNET-v2-Depth": {
        "keys": {},
        "source": "UNET-v2-Depth.txt",
        "prefix": "model.diffusion_model."
    },
    "UNET-v2-Refiner": {
        "keys": {},
        "source": "UNET-v2-Refiner.txt",
        "prefix": "model.diffusion_model."
    },
    "UNET-XL-SD": {
        "keys": {},
        "source": "UNET-XL-SD.txt",
        "prefix": "model.diffusion_model."
    },
    "UNET-XL-B-SD": {
        "keys": {},
        "source": "UNET-XL-B-SD.txt",
        "prefix": "model.diffusion_model."
    },
    "UNET-XL-Refiner": {
        "keys": {},
        "source": "UNET-XL-Refiner.txt",
        "prefix": "model.diffusion_model."
    },
    "UNET-XL-Inpainting": {
        "keys": {},
        "source": "UNET-XL-Inpainting.txt",
        "prefix": "model.diffusion_model."
    },
    "UNET-XL-A-MAIN": {
        "keys": {},
        "source": "UNET-XL-A-MAIN.txt",
        "prefix": "model.diffusion_model."
    },
    "UNET-XL-B-Inpainting": {
        "keys": {},
        "source": "UNET-XL-B-Inpainting.txt",
        "prefix": "model.diffusion_model."
    },
    "UNET-XL-UP": {
        "keys": {},
        "source": "UNET-v1-UP.txt",
        "prefix": "model_ema.diffusion_model."
    },
    "UNET-XL-DOWN": {
        "keys": {},
        "source": "UNET-XL-DOWN.txt",
        "prefix": "model_ema.diffusion_model."
    },
    "UNET-v3-MMDIT": {
        "keys": {},
        "source": "UNET-v3-MMDIT.txt",
        "prefix": "model.diffusion_model."
    },
#    "UNET-XL-SKIP": {
#        "keys": {},
#        "source": "UNET-v1-SKIP.txt",
#        "prefix": ""
#    },
#    "UNET-XL-EMBLAY": {
#        "keys": {},
#        "source": "UNET-v1-EMBLAY.txt",
#        "prefix": ""
#    },
#    "UNET-XL-TIME-EMB": {
#        "keys": {},
#        "source": "UNET-v1-TIME-EMB.txt",
#        "prefix": ""
#    },
#    "UNET-XL-MID": {
#        "keys": {},
#        "source": "UNET-v1-MID.txt",
#        "prefix": ""
#    },
    "VAE-v1-SD": {
        "keys": {},
        "source": "VAE-v1-SD.txt",
        "prefix": "first_stage_model."
    },
    "VAE-v3-SD": {
        "keys": {},
        "source": "VAE-v3-SD.txt",
        "prefix": "first_stage_model."
    },
    "VAE-vX-S": {
        "keys": {},
        "source": "VAE-vX-S.txt",
        "prefix": "first_stage_model."
    },
    "VAE-vX-D": {
        "keys": {},
        "source": "VAE-vX-D.txt",
        "prefix": "first_stage_model."
    },
    "CLIP-v1-SD": {
        "keys": {},
        "source": "CLIP-v1-SD.txt",
        "prefix": "cond_stage_model.transformer.text_model."
    },
    "CLIP-v1-NAI": {
        "keys": {},
        "source": "CLIP-v1-SD.txt",
        "prefix": "cond_stage_model.transformer."
    },
    "CLIP-v1-SCPR": {
        "keys": {},
        "source": "CLIP-v1-SCPR.txt",
        "prefix": "cond_stage_model."
    },
    "CLIP-v1-POS": {
        "keys": {},
        "source": "CLIP-v1-POS.txt",
        "prefix": "cond_stage_model."
    },
    "CLIP-v1-EMBED": {
        "keys": {},
        "source": "CLIP-v1-SD.txt",
        "prefix": "embedding_manager.embedder.transformer.text_model."
    },
    "CLIP-v1-TOKEN": {
        "keys": {},
        "source": "CLIP-v1-TOKEN.txt",
        "prefix": "cond_stage_model.transformer.text_model."
    },
    #"CLIP-v1-DIFF": {
    #    "keys": {},
    #    "source": "CLIP-v1-DIFF.txt",
    #    "prefix": "text_model."
    #},
    "CLIP-v2-SD": {
        "keys": {},
        "source": "CLIP-v2-SD.txt",
        "prefix": "cond_stage_model.model."
    },
    "CLIP-v2-WD": {
        "keys": {},
        "source": "CLIP-v2-WD.txt",
        "prefix": "cond_stage_model.model."
    },
    "CLIP-XL": {
        "keys": {},
        "source": "CLIP-XL-SD.txt",
        "prefix": "conditioner.embedders.1.model."
    },
    "CLIP-XL-Refiner": {
        "keys": {},
        "source": "CLIP-XL-SD.txt",
        "prefix": "conditioner.embedders.1.model."
    },
    "CLIP-XL-AUX": {
        "keys": {},
        "source": "CLIP-v1-SD.txt",
        "prefix": "conditioner.embedders.0.transformer.text_model."
    },
    "CLIP-XL-AUZ": {
        "keys": {},
        "source": "CLIP-v1-SD.txt",
        "prefix": "conditioner.embedders.2.transformer.text_model."
    },
    "CLIP-XL-SCPR": {
        "keys": {},
        "source": "CLIP-v1-SCPR.txt",
        "prefix": "conditioner.embedders.0.transformer.text_model."
    },
    "CLIP-XL-POS": {
        "keys": {},
        "source": "CLIP-v1-POS.txt",
        "prefix": "conditioner.embedders.0.transformer.text_model."
    },
    "CLIP-XL-TOKEN": {
        "keys": {},
        "source": "CLIP-XL-TOKEN.txt",
        "prefix": "conditioner.embedders.1.model."
    },
    #"CLIP-XL-DIFF": {
    #    "keys": {},
    #    "source": "CLIP-XL-DIFF.txt",
    #    "prefix": ""
    #},
    "CLIP-XL-TOKEN": {
        "keys": {},
        "source": "CLIP-XL-TOKEN.txt",
        "prefix": "conditioner.embedders.1.model."
    },
    "CLIP-AUX-TOKEN": {
        "keys": {},
        "source": "CLIP-AUX-TOKEN.txt",
        "prefix": "conditioner.embedders.0.model."
    },
    "CLIP-XL-TOKEMB": {
        "keys": {},
        "source": "CLIP-XL-TOKEMB.txt",
        "prefix": ""
    },
    "CLIP-v3-G": {
        "keys": {},
        "source": "CLIP-v3-G.txt",
        "prefix": "text_encoders.clip_g.transformer."
    },
    #"CLIP-v3-GB": {
    #    "keys": {},
    #    "source": "CLIP-v3-GB.txt",
    #    "prefix": "text_encoders.clip_g.transformer.text_model."
    #},
    #"CLIP-v3-GP": {
    #    "keys": {},
    #    "source": "CLIP-v3-GP.txt",
    #    "prefix": "text_encoders.clip_g.transformer."
    #},
    "CLIP-v3-L": {
        "keys": {},
        "source": "CLIP-v3-L.txt",
        "prefix": "text_encoders.clip_l.transformer."
    },
    "CLIP-v3-T5": {
        "keys": {},
        "source": "CLIP-v3-T5.txt",
        "prefix": "text_encoders.t5xxl.transformer."
    },
    "Depth-v2-SD": {
        "keys": {},
        "source": "Depth-v2-SD.txt",
        "prefix": "depth_model.model."
    },
    "LoRA-v1-CLIP": {
        "keys": {},
        "shapes": {},
        "source": "LoRA-v1-CLIP.txt",
        "prefix": ""
    },
    "LoRA-v1A-CLIP": {
        "keys": {},
        "shapes": {},
        "source": "LoRA-v1A-CLIP.txt",
        "prefix": ""
    },
    "LoRA-XL-CLIP": {
        "keys": {},
        "shapes": {},
        "source": "LoRA-XL-CLIP.txt",
        "prefix": ""
    },
    "LoRA-XL-AUX-CLIP": {
        "keys": {},
        "shapes": {},
        "source": "LoRA-XL-AUX-CLIP.txt",
        "prefix": ""
    },
    "LyCO-XL-CLIP": {
        "keys": {},
        "shapes": {},
        "source": "LyCO-XL-CLIP.txt",
        "prefix": ""
    },
    "LyCO-XL-AUX-CLIP": {
        "keys": {},
        "shapes": {},
        "source": "LyCO-XL-AUX-CLIP.txt",
        "prefix": ""
    },
    "LoRA-v1-UNET": {
        "keys": {},
        "shapes": {},
        "source": "LoRA-v1-UNET.txt",
        "prefix": ""
    },
    "LoRA-v1A-UNET": {
        "keys": {},
        "shapes": {},
        "source": "LoRA-v1A-UNET.txt",
        "prefix": ""
    },
    "LoRA-XL-UNET": {
        "keys": {},
        "shapes": {},
        "source": "LoRA-XL-UNET.txt",
        "prefix": ""
    },
    "LoRA-XL-UNET-S": {
        "keys": {},
        "shapes": {},
        "source": "LoRA-XL-UNET-S.txt",
        "prefix": ""
    },
    "LoRA-XL-UNET-M": {
        "keys": {},
        "shapes": {},
        "source": "LoRA-XL-UNET-M.txt",
        "prefix": ""
    },
    "LoRA-XL-UNET-D": {
        "keys": {},
        "shapes": {},
        "source": "LoRA-XL-UNET-D.txt",
        "prefix": ""
    },
    "LyCO-XL-UNET": {
        "keys": {},
        "shapes": {},
        "source": "LyCO-XL-UNET.txt",
        "prefix": ""
    },
    "ControlNet-v1-SD": {
        "keys": {},
        "shapes": {},
        "source": "ControlNet-v1-SD.txt",
        "prefix": "control_model."
    },
    "Clipvision-G": {
        "keys": {},
        "shapes": {},
        "source": "Clipvision-G.txt",
        "prefix": ""
    },
}

COMPONENT_CLASS = {
    "UNET-v1-SD": "UNET-v1",
    "UNET-v1-UP": "UNET-v1-UP",
    "UNET-v1-DOWN": "UNET-v1-DOWN",
    "UNET-v1-EMA": "EMA-UNET-v1",
    "UNET-v1-Inpainting": "UNET-v1",
    "UNET-v1-Pix2Pix": "UNET-v1-Pix2Pix",
    "UNET-v1-Pix2Pix-EMA": "EMA-UNET-v1-Pix2Pix",
    "UNET-v1-SKIP": "UNET-v1-SKIP",
    "UNET-v1-EMBLAY": "UNET-v1-EMBLAY",
    "UNET-v1-TIME-EMB": "UNET-v1-TIME-EMB",
    "UNET-v1-MID": "UNET-v1-MID",
    "UNET-v2-SD": "UNET-v2",
    "UNET-v2-Inpainting": "UNET-v2",
    "UNET-v2-Depth": "UNET-v2-Depth",
    "UNET-v2-Refiner": "UNET-v2-Refiner",
    "UNET-v3-MMDIT": "UNET-v3-MMDIT",
    "UNET-XL-SD": "UNET-XL",
    "UNET-XL-B-SD": "UNET-XL-B-SD",
    "UNET-XL-Refiner": "UNET-XL-Refiner",
    "UNET-XL-Inpainting": "UNET-XL-Inpainting",
    "UNET-XL-A-MAIN": "UNET-XL-A-MAIN",
    "UNET-XL-B-Inpainting": "UNET-XL-B-Inpainting",
    "UNET-XL-UP": "UNET-XL-UP",
    "UNET-XL-DOWN": "UNET-XL-DOWN",
    "UNET-XL-SKIP": "UNET-XL-SKIP",
    "UNET-XL-EMBLAY": "UNET-XL-EMBLAY",
    "UNET-XL-TIME-EMB": "UNET-XL-TIME-EMB",
    "UNET-XL-MID": "UNET-XL-MID",
    "VAE-v1-SD": "VAE-v1",
    "VAE-v3-SD": "VAE-v3",
    "VAE-vX-S": "VAE-vX-S",
    "VAE-vX-D": "VAE-vX-D",
    "CLIP-v1-SD": "CLIP-v1",
    "CLIP-v1-NAI": "CLIP-v1",
    "CLIP-v1-SCPR": "CLIP-v1-SCPR",
    "CLIP-v1-POS": "CLIP-v1-POS",
    "CLIP-v1-EMBED": "CLIP-v1",
    "CLIP-v1-TOKEN": "CLIP-TOKEN",
    "CLIP-v2-SD": "CLIP-v2",
    "CLIP-v2-WD": "CLIP-v2",
    "CLIP-v3-L": "CLIP-v3-L",
    "CLIP-v3-G": "CLIP-v3-G",
    # "CLIP-v3-GB": "CLIP-v3-GB",
    # "CLIP-v3-GP": "CLIP-v3-GP",
    "CLIP-v3-T5": "CLIP-v3-T5",
    "CLIP-XL": "CLIP-XL",
    "CLIP-XL-Refiner": "CLIP-XL",
    "CLIP-XL-AUX": "CLIP-XL-AUX",
    "CLIP-XL-AUZ": "CLIP-XL-AUZ",
    "CLIP-XL-SCPR": "CLIP-XL-SCPR",
    "CLIP-XL-POS": "CLIP-XL-POS",
    "CLIP-XL-TOKEN": "CLIP-XL-TOKEN",
    "CLIP-AUX-TOKEN": "CLIP-AUX-TOKEN",
    "CLIP-XL-TOKEMB": "CLIP-XL-TOKEMB",
    "Depth-v2-SD": "Depth-v2",
    "LoRA-v1-UNET": "LoRA-v1-UNET",
    "LoRA-v1-CLIP": "LoRA-v1-CLIP",
    "LoRA-v1A-UNET": "LoRA-v1A-UNET",
    "LoRA-v1A-CLIP": "LoRA-v1A-CLIP",
    "LoRA-XL-UNET": "LoRA-XL-UNET",
    "LoRA-XL-UNET-S": "LoRA-XL-UNET-S",
    "LoRA-XL-UNET-M": "LoRA-XL-UNET-M",
    "LoRA-XL-UNET-D": "LoRA-XL-UNET-D",
    "LoRA-XL-UNET-SD": "LoRA-XL-UNET-SD",
    "LoRA-XL-CLIP": "LoRA-XL-CLIP",
    "LoRA-XL-AUX-CLIP": "LoRA-XL-AUX-CLIP",
    "LyCO-XL-UNET": "LyCO-XL-UNET",
    "LyCO-XL-CLIP": "LyCO-XL-CLIP",
    "LyCO-XL-AUX-CLIP": "LyCO-XL-AUX-CLIP",
    "ControlNet-v1-SD": "ControlNet-v1",
    "Clipvision-G": "Clipvision-G",
}

OPTIONAL = [
    ("alphas_cumprod", (1000,)),
    ("alphas_cumprod_prev", (1000,)),
    ("betas", (1000,)),
    ("log_one_minus_alphas_cumprod", (1000,)),
    ("model_ema.decay", ()),
    ("model_ema.num_updates", ()),
    ("posterior_log_variance_clipped", (1000,)),
    ("posterior_mean_coef1", (1000,)),
    ("posterior_mean_coef2", (1000,)),
    ("posterior_variance", (1000,)),
    ("sqrt_alphas_cumprod", (1000,)),
    ("sqrt_one_minus_alphas_cumprod", (1000,)),
    ("sqrt_recip_alphas_cumprod", (1000,)),
    ("sqrt_recipm1_alphas_cumprod", (1000,)),
    ("logvar", (1000,)),
    ("visual_projection.weight", (1280,1664,)),
    ("logit_scale", ()),
    ("text_projection", (768,768,)),
    ("embeddings.position_ids", (1,77,)),
    ("positional_embedding", (248,768,)),
    ("positional_embedding_res", (248,768,)),
]

ARCHITECTURES = {
    "UNET-v1": {
        "classes": ["UNET-v1"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "UNET-v1-UP": {
        "classes": ["UNET-v1-UP"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "UNET-v1-DOWN": {
        "classes": ["UNET-v1-DOWN"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "UNET-v1-Pix2Pix": {
        "classes": ["UNET-v1-Pix2Pix"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
#    "UNET-v1-MID": {
#        "classes": ["UNET-v1-MID"],
#        "optional": [],
#        "required": [],
#        "prefixed": False
#    },
#    "UNET-v1-TIME-EMB": {
#        "classes": ["UNET-v1-TIME-EMB"],
#        "optional": [],
#        "required": [],
#        "prefixed": False
#    },
#    "UNET-v1-EMBLAY": {
#        "classes": ["UNET-v1-EMBLAY"],
#        "optional": [],
#        "required": [],
#        "prefixed": False
#    },
#    "UNET-v1-SKIP": {
#        "classes": ["UNET-v1-SKIP"],
#        "optional": [],
#        "required": [],
#        "prefixed": False
#    },
    "UNET-v2": {
        "classes": ["UNET-v2"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "UNET-v2-Depth": {
        "classes": ["UNET-v2-Depth"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "UNET-v2-Refiner": {
        "classes": ["UNET-v2-Refiner"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "UNET-v3-MMDIT": {
        "classes": ["UNET-v3-MMDIT"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "UNET-XL": {
        "classes": ["UNET-XL"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "UNET-XL-B-SD": {
        "classes": ["UNET-XL-B-SD"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "UNET-XL-Refiner": {
        "classes": ["UNET-XL-Refiner"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "UNET-XL-Inpainting": {
        "classes": ["UNET-XL-Inpainting"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "UNET-XL-A-MAIN": {
        "classes": ["UNET-XL-A-MAIN"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "UNET-XL-B-Inpainting": {
        "classes": ["UNET-XL-B-Inpainting"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "UNET-XL-UP": {
        "classes": ["UNET-XL-UP"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "UNET-XL-DOWN": {
        "classes": ["UNET-XL-DOWN"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
#    "UNET-XL-MID": {
#        "classes": ["UNET-XL-MID"],
#        "optional": [],
#        "required": [],
#        "prefixed": False
#    },
#    "UNET-XL-TIME-EMB": {
#        "classes": ["UNET-XL-TIME-EMB"],
#        "optional": [],
#        "required": [],
#        "prefixed": False
#    },
#    "UNET-XL-EMBLAY": {
#        "classes": ["UNET-XL-EMBLAY"],
#        "optional": [],
#        "required": [],
#        "prefixed": False
#    },
#    "UNET-XL-SKIP": {
#        "classes": ["UNET-XL-SKIP"],
#        "optional": [],
#        "required": [],
#        "prefixed": False
#    },
    "LoRA-v1-UNET": {
        "classes": ["LoRA-v1-UNET"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "LoRA-v1A-UNET": {
        "classes": ["LoRA-v1A-UNET"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "LoRA-XL-UNET": {
        "classes": ["LoRA-XL-UNET"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "LoRA-XL-UNET-SD": {
        "classes": ["LoRA-XL-UNET-S", "LoRA-XL-UNET-D"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "LoRA-XL-UNET-S": {
        "classes": ["LoRA-XL-UNET-S"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "LoRA-XL-UNET-M": {
        "classes": ["LoRA-XL-UNET-M"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "LoRA-XL-UNET-D": {
        "classes": ["LoRA-XL-UNET-D"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "LyCO-XL-UNET": {
        "classes": ["LyCO-XL-UNET"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "VAE-v1": {
        "classes": ["VAE-v1"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "VAE-vX-S": {
        "classes": ["VAE-vX-S"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "VAE-vX-D": {
        "classes": ["VAE-vX-D"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "CLIP-v1": {
        "classes": ["CLIP-v1"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "CLIP-v1-SCPR": {
        "classes": ["CLIP-v1-SCPR"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "CLIP-v1-POS": {
        "classes": ["CLIP-v1-POS"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "CLIP-v1-EMBED": {
        "classes": ["CLIP-v1-EMBED"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "CLIP-v1-TOKEN": {
        "classes": ["CLIP-v1-TOKEN"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "CLIP-v1-DUAL": {
        "classes": ["CLIP-v1-SD", "CLIP-v1-EMBED"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "CLIP-v2": {
        "classes": ["CLIP-v2"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "CLIP-v3-L": {
        "classes": ["CLIP-v3-L"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "CLIP-v3-G": {
        "classes": ["CLIP-v3-G"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    # "CLIP-v3-GB": {
    #     "classes": ["CLIP-v3-GB"],
    #     "optional": [],
    #     "required": [],
    #     "prefixed": False
    # },
    # "CLIP-v3-GP": {
    #     "classes": ["CLIP-v3-GP"],
    #     "optional": [],
    #     "required": [],
    #     "prefixed": False
    # },
    "CLIP-v3-T5": {
        "classes": ["CLIP-v3-T5"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "CLIP-XL": {
        "classes": ["CLIP-XL"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "CLIP-XL-AUX": {
        "classes": ["CLIP-XL-AUX"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "CLIP-XL-AUZ": {
        "classes": ["CLIP-XL-AUZ"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "CLIP-XL-SCPR": {
        "classes": ["CLIP-XL-SCPR"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "CLIP-XL-POS": {
        "classes": ["CLIP-XL-POS"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "CLIP-XL-TOKEN": {
        "classes": ["CLIP-XL-TOKEN"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "CLIP-AUX-TOKEN": {
        "classes": ["CLIP-AUX-TOKEN"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "CLIP-XL-TOKEMB": {
        "classes": ["CLIP-XL-TOKEMB"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "LoRA-v1-CLIP": {
        "classes": ["LoRA-v1-CLIP"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "LoRA-v1A-CLIP": {
        "classes": ["LoRA-v1A-CLIP"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "LoRA-XL-CLIP": {
        "classes": ["LoRA-XL-CLIP"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "LoRA-XL-AUX-CLIP": {
        "classes": ["LoRA-XL-AUX-CLIP"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "LyCO-XL-CLIP": {
        "classes": ["LyCO-XL-CLIP"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "LyCO-XL-AUX-CLIP": {
        "classes": ["LyCO-XL-AUX-CLIP"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "Depth-v2": {
        "classes": ["Depth-v2"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "ControlNet-v1": {
        "classes": ["ControlNet-v1"],
        "optional": [],
        "required": [],
        "prefixed": False
    },
    "Clipvision-G": {
        "classes": ["Clipvision-G"],
        "optional": [],
        "required": [],
        "prefixed": True
    },
    "SD-UNET-XL-SD": {
        "classes": ["UNET-XL-A-MAIN", "UNET-XL-B-SD"],
        "optional": OPTIONAL,
        "required": [],
        "prefixed": False
    },
    "SD-UNET-XL-Inpainting": {
        "classes": ["UNET-XL-A-MAIN", "UNET-XL-B-Inpainting"],
        "optional": OPTIONAL,
        "required": [],
        "prefixed": False
    },
    "SD-vX-VAE": {
        "classes": ["VAE-vX-S", "VAE-vX-D"],
        "optional": OPTIONAL,
        "required": [],
        "prefixed": False
    },
    "SD-v1": {
        "classes": ["UNET-v1", "VAE-v1", "CLIP-v1"],
        "optional": OPTIONAL,
        "required": [],
        "prefixed": True
    },
    "SD-v1-ALT": {
        "classes": ["UNET-v1-UP", "UNET-v1-DOWN", "VAE-v1", "CLIP-v1"],
        "optional": OPTIONAL,
        "required": [],
        "prefixed": True
    },
    "SD-v1-SCPR": {
        "classes": ["UNET-v1", "VAE-v1", "CLIP-v1", "CLIP-v1-SCPR"],
        "optional": OPTIONAL,
        "required": [],
        "prefixed": True
    },
    "SD-v1-DualCLIP": {
        "classes": ["UNET-v1", "VAE-v1", "CLIP-v1", "CLIP-v1-EMBED"],
        "optional": OPTIONAL,
        "required": [],
        "prefixed": True
    },
    "SD-v1-Pix2Pix": {
        "classes": ["UNET-v1-Pix2Pix", "VAE-v1", "CLIP-v1"],
        "optional": OPTIONAL,
        "required": [],
        "prefixed": True
    },
    "SD-v1-ControlNet": {
        "classes": ["UNET-v1", "VAE-v1", "CLIP-v1", "ControlNet-v1"],
        "optional": OPTIONAL,
        "required": [],
        "prefixed": True
    },
    "SD-v2": {
        "classes": ["UNET-v2", "VAE-v1", "CLIP-v2"],
        "optional": OPTIONAL,
        "required": [],
        "prefixed": True
    },
    "SD-v2-Depth": {
        "classes": ["UNET-v2-Depth", "VAE-v1", "CLIP-v2", "Depth-v2"],
        "optional": OPTIONAL,
        "required": [],
        "prefixed": True
    },
    "SD-v2-Refiner": {
        "classes": ["UNET-v2-Refiner", "VAE-v1", "CLIP-v2"],
        "optional": OPTIONAL,
        "required": [],
        "prefixed": True
    },
    "SD-v3-Triple": {
        "classes": ["UNET-v3-MMDIT", "VAE-v3", "CLIP-v3-L", "CLIP-v3-G", "CLIP-v3-T5"],
        "optional": OPTIONAL,
        "required": [],
        "prefixed": True
    },
    "SD-v3-Dual": {
        "classes": ["UNET-v3-MMDIT", "VAE-v3", "CLIP-v3-L", "CLIP-v3-G"],
        "optional": OPTIONAL,
        "required": [],
        "prefixed": True
    },
    "SD-XL": {
        "classes": ["UNET-XL", "VAE-v1", "CLIP-XL", "CLIP-XL-AUX"],
        "optional": OPTIONAL,
        "required": [],
        "prefixed": True
    },
    "SD-XL-Refiner": {
        "classes": ["UNET-XL-Refiner", "VAE-v1", "CLIP-XL"],
        "optional": OPTIONAL,
        "required": [],
        "prefixed": True
    },
    "SD-XL-Inpainting": {
        "classes": ["UNET-XL-Inpainting", "VAE-v1", "CLIP-XL", "CLIP-XL-AUX"],
        "optional": OPTIONAL,
        "required": [],
        "prefixed": True
    },
    "SD-XL-TriCLIP": {
        "classes": ["UNET-XL", "VAE-v1", "CLIP-XL", "CLIP-XL-AUX", "CLIP-XL-AUZ"],
        "optional": OPTIONAL,
        "required": [],
        "prefixed": True
    },
#    "SD-XL-FIX": {
#        "classes": ["UNET-XL", "VAE-v1", "CLIP-XL", "CLIP-XL-AUX", "VAE-vX-S"],
#        "optional": OPTIONAL,
#        "required": [],
#        "prefixed": True
#    },
    "SD-XL-ALT": {
        "classes": ["UNET-XL-UP", "UNET-XL-DOWN", "VAE-v1", "CLIP-XL", "CLIP-XL-AUX"],
        "optional": OPTIONAL,
        "required": [],
        "prefixed": True
    },
#    "SD-XL-LoRAXL-CLIP": {
#        "classes": ["LoRA-XL-CLIP", "LoRA-XL-AUX-CLIP"],
#        "optional": OPTIONAL,
#        "required": [],
#        "prefixed": True
#    },
#    "SD-XL-LoRAUX-CLIP": {
#        "classes": ["LoRA-XL-AUX-CLIP"],
#        "optional": OPTIONAL,
#        "required": [],
#        "prefixed": True
#    },
    "EMA-v1": {
        "classes": ["EMA-UNET-v1"],
        "optional": OPTIONAL,
        "required": [],
        "prefixed": True
    },
    "EMA-v1-Pix2Pix": {
        "classes": ["EMA-UNET-v1-Pix2Pix"],
        "optional": OPTIONAL,
        "required": [],
        "prefixed": True
    },
    "SD-v1-UNET": {
        "classes": ["UNET-v1-UP", "UNET-v1-DOWN"],
        "optional": OPTIONAL,
        "required": [],
        "prefixed": True
    },
    "SD-XL-UNET": {
        "classes": ["UNET-XL-UP", "UNET-XL-DOWN"],
        "optional": OPTIONAL,
        "required": [],
        "prefixed": True
    },
    "LoRA-v1": {
        "classes": ["LoRA-v1-CLIP", "LoRA-v1-UNET"],
        "optional": OPTIONAL,
        "required": [],
        "prefixed": True
    },
    "LoRA-v1A": {
        "classes": ["LoRA-v1A-CLIP", "LoRA-v1A-UNET"],
        "optional": OPTIONAL,
        "required": [],
        "prefixed": True
    },
    "LoRA-XL": {
        "classes": ["LoRA-XL-CLIP", "LoRA-XL-AUX-CLIP", "LoRA-XL-UNET"],
        "optional": OPTIONAL,
        "required": [],
        "prefixed": True
    },
    "LoRA-XL-S": {
        "classes": ["LoRA-XL-CLIP", "LoRA-XL-AUX-CLIP", "LoRA-XL-UNET-S"],
        "optional": OPTIONAL,
        "required": [],
        "prefixed": True
    },
    "LoRA-XL-M": {
        "classes": ["LoRA-XL-CLIP", "LoRA-XL-AUX-CLIP", "LoRA-XL-UNET-M"],
        "optional": OPTIONAL,
        "required": [],
        "prefixed": True
    },
    "LoRA-XL-SD": {
        "classes": ["LoRA-XL-CLIP", "LoRA-XL-AUX-CLIP", "LoRA-XL-UNET-SD"],
        "optional": OPTIONAL,
        "required": [],
        "prefixed": True
    },
    "LyCO-XL": {
        "classes": ["LyCO-XL-CLIP", "LyCO-XL-AUX-CLIP", "LyCO-XL-UNET"],
        "optional": OPTIONAL,
        "required": [],
        "prefixed": True
    },
    "LoRA-XL-TE": {
        "classes": ["LoRA-XL-CLIP", "LoRA-XL-AUX-CLIP"],
        "optional": OPTIONAL,
        "required": [],
        "prefixed": True
    },
    "LyCO-XL-TE": {
        "classes": ["LyCO-XL-CLIP", "LyCO-XL-AUX-CLIP"],
        "optional": OPTIONAL,
        "required": [],
        "prefixed": True
    },
    # standalone component architectures, for detecting broken models
    "UNET-v1-BROKEN": {
        "classes": ["UNET-v1"],
        "optional": [],
        "required": [],
        "prefixed": True
    },
    "UNET-v1-Pix2Pix-BROKEN": {
        "classes": ["UNET-v1-Pix2Pix"],
        "optional": [],
        "required": [],
        "prefixed": True
    },
    "UNET-v2-BROKEN": {
        "classes": ["UNET-v2"],
        "optional": [],
        "required": [],
        "prefixed": True
    },
    "UNET-v2-Depth-BROKEN": {
        "classes": ["UNET-v2-Depth"],
        "optional": [],
        "required": [],
        "prefixed": True
    },
    "UNET-v2-Refiner-BROKEN": {
        "classes": ["UNET-v2-Refiner"],
        "optional": [],
        "required": [],
        "prefixed": True
    },
    "UNET-v3-MMDIT-BROKEN": {
        "classes": ["UNET-v3-MMDIT"],
        "optional": [],
        "required": [],
        "prefixed": True
    },
    "UNET-XL-BROKEN": {
        "classes": ["UNET-XL"],
        "optional": [],
        "required": [],
        "prefixed": True
    },
    "UNET-XL-Refiner-BROKEN": {
        "classes": ["UNET-XL-Refiner"],
        "optional": [],
        "required": [],
        "prefixed": True
    },
    "UNET-XL-Inpainting-BROKEN": {
        "classes": ["UNET-XL-Inpainting"],
        "optional": [],
        "required": [],
        "prefixed": True
    },
    "VAE-v1-BROKEN": {
        "classes": ["VAE-v1"],
        "optional": [],
        "required": [],
        "prefixed": True
    },
    "VAE-v3-BROKEN": {
        "classes": ["VAE-v3"],
        "optional": [],
        "required": [],
        "prefixed": True
    },
    "CLIP-v1-BROKEN": {
        "classes": ["CLIP-v1"],
        "optional": [],
        "required": [],
        "prefixed": True
    },
    "CLIP-v1-SCPR-BROKEN": {
        "classes": ["CLIP-v1-SCPR"],
        "optional": [],
        "required": [],
        "prefixed": True
    },
    "CLIP-v1-EMBED-BROKEN": {
        "classes": ["CLIP-v1-EMBED"],
        "optional": [],
        "required": [],
        "prefixed": True
    },
    "CLIP-v2-BROKEN": {
        "classes": ["CLIP-v2"],
        "optional": [],
        "required": [],
        "prefixed": True
    },
    "CLIP-v3-L-BROKEN": {
        "classes": ["CLIP-v3-L"],
        "optional": [],
        "required": [],
        "prefixed": True
    },
    "CLIP-v3-G-BROKEN": {
        "classes": ["CLIP-v3-G"],
        "optional": [],
        "required": [],
        "prefixed": True
    },
    "CLIP-v3-T5-BROKEN": {
        "classes": ["CLIP-v3-T5"],
        "optional": [],
        "required": [],
        "prefixed": True
    },
    "Depth-v2-BROKEN": {
        "classes": ["Depth-v2"],
        "optional": [],
        "required": [],
        "prefixed": True
    },
    "ControlNet-v1-BROKEN": {
        "classes": ["ControlNet-v1"],
        "optional": [],
        "required": [],
        "prefixed": True
    },
}

def tensor_size(t):
    if type(t) == torch.Tensor:
        return t.nelement() * t.element_size()
    return 0

def tensor_shape(key, data):
    if hasattr(data, 'shape'):
        shape = tuple(data.shape)
        for c in ["LoRA-v1-UNET", "LoRA-v1-CLIP", "LoRA-v1A-CLIP", "LoRA-v1A-UNET", "LoRA-XL-CLIP", "LoRA-XL-AUX-CLIP", "LoRA-XL-UNET", "LoRA-XL-UNET-S", "LoRA-XL-UNET-M", "LoRA-XL-UNET-D", "LyCO-XL-CLIP", "LyCO-XL-AUX-CLIP", "LyCO-XL-UNET"]:
            if key in COMPONENTS[c]['shapes']:
                lora_shape = COMPONENTS[c]['shapes'][key]
                if len(shape) == len(lora_shape):
                    shape = tuple(a if b != -1 else b for a, b in zip(shape, lora_shape))
        return shape
    return tuple()

def load_components(path):
    for c in COMPONENTS:
        file = os.path.join(path, COMPONENTS[c]["source"])
        if not os.path.exists(file):
            print(f"CANNOT FIND {c} KEYS")
        with open(file, 'r') as f:
            COMPONENTS[c]["keys"] = set()
            for l in f:
                l = l.rstrip().split(" ")
                k, z = l[0], l[1]
                z = z[1:-1].split(",")
                if not z[0]:
                    z = tuple()
                else:
                    z = tuple(int(i) for i in z)
                COMPONENTS[c]["keys"].add((k,z))
                if "shapes" in COMPONENTS[c]:
                    COMPONENTS[c]["shapes"][k] = z

def get_prefixed_keys(component):
    prefix = COMPONENTS[component]["prefix"]
    allowed = COMPONENTS[component]["keys"]
    return set([(prefix + k, z) for k, z in allowed])

def get_keys_size(model, keys):
    z = 0
    for k in keys:
        if k in model:
            z += tensor_size(model[k])
    return z

class FakeTensor():
    def __init__(self, shape):
        self.shape = shape

def build_fake_model(model):
    fake_model = {}
    for k in model:
        fake_model[k] = FakeTensor(tensor_shape(k, model[k]))
    return fake_model

def inspect_model(model, all=False):
    # find all arch's and components in the model
    # also reasons for failing to find them

    keys = set([(k, tensor_shape(k, model[k])) for k in model])

    rejected = {}

    components = [] # comp -> prefixed
    classes = {} # class -> [comp]
    for comp in COMPONENTS:
        required_keys_unprefixed = COMPONENTS[comp]["keys"]
        required_keys_prefixed = get_prefixed_keys(comp)
        missing_unprefixed = required_keys_unprefixed.difference(keys)
        missing_prefixed = required_keys_prefixed.difference(keys)

        if not missing_unprefixed:
            components += [(comp, False)]
        if not missing_prefixed:
            components += [(comp, True)]

        if missing_prefixed and missing_unprefixed:
            if missing_prefixed != required_keys_prefixed:
                rejected[comp] = rejected.get(comp, []) + [{"reason": f"Missing required keys ({len(missing_prefixed)} of {len(required_keys_prefixed)})", "data": list(missing_prefixed)}]
            
            if missing_unprefixed != required_keys_unprefixed:
                rejected[comp] = rejected.get(comp, []) + [{"reason": f"Missing required keys ({len(missing_unprefixed)} of {len(required_keys_unprefixed)})", "data": list(missing_unprefixed)}]
        else:
            clss = COMPONENT_CLASS[comp]
            classes[clss] = [comp] + classes.get(clss, [])
    
    

    found = {} # arch -> {class -> [comp]}
    for arch in ARCHITECTURES:
        needs_prefix = ARCHITECTURES[arch]["prefixed"]
        required_classes = set(ARCHITECTURES[arch]["classes"])
        required_keys = set(ARCHITECTURES[arch]["required"])

        if not required_keys.issubset(keys):
            missing = required_keys.difference(keys)
            if missing != required_keys:
                rejected[arch] = rejected.get(arch, []) + [{"reason": f"Missing required keys ({len(missing)} of {len(required_keys)})", "data": list(missing)}]
            continue

        found_classes = {}
        for clss in required_classes:
            if clss in classes:
                for comp in classes[clss]:
                    
                    if (comp, needs_prefix) in components:# or ((comp, not needs_prefix) in components and not needs_prefix):
                        found_classes[clss] = found_classes.get(clss, [])
                        found_classes[clss] += [comp]
                    #else:
                    #    rejected[arch] = rejected.get(arch, []) + [{"reason": "Class has incorrect prefix", "data": [clss]}]

        found_class_names = set(found_classes.keys())
        if not required_classes.issubset(found_class_names):
            if found_class_names:
                missing = list(required_classes.difference(found_class_names))
                rejected[arch] = rejected.get(arch, []) + [{"reason": "Missing required classes", "data": missing}]
            continue

        found[arch] = found_classes

    # if we found a real architecture then dont show the broken ones
    if any([a.startswith("SD-") for a in found]):
        for a in list(found.keys()):
            if a.endswith("-BROKEN"):
                del found[a]
    
    for arch in list(found.keys()):
        if "LoRA" in arch:
            for clss in found[arch]:
                if len(found[arch][clss]) == 2:
                    found[arch][clss] = [found[arch][clss][0].replace("-v1-", "-v1A-")]
    
    if "LoRA-v1" in found:
        del found["LoRA-v1-UNET"]
        del found["LoRA-v1-CLIP"]

    if all:
        return found, rejected
    else:
        return resolve_arch(found)

def resolve_class(components):
    components = list(components)

    if not components or len(components) == 1:
        return components

    # prefer SD components vs busted ass components
    sd_components = [c for c in components if "SD" in c]
    if len(sd_components) == 1:
        return [sd_components[0]]

    # otherwise component with the most keys is probably the best
    components = sorted(components, key=lambda c: len(COMPONENTS[c]["keys"]), reverse=True)

    return [components[0]]

def resolve_arch(arch):
    arch = copy.deepcopy(arch)
    # resolve potentially many overlapping arch's to a single one

    if not arch:
        return {}

    # select arch with most keys
    arch_sizes = {}
    for a in arch:
        arch_sizes[a] = len(ARCHITECTURES[a]["required"])
        for clss in arch[a]:
            arch[a][clss] = resolve_class(arch[a][clss])
            if arch[a][clss]:
                arch_sizes[a] += len(COMPONENTS[arch[a][clss][0]]["keys"])
    for normal in ["SD-v1", "SD-v2"]:
        if normal in arch_sizes:
            choosen = normal
            break
    else:
        choosen = max(arch_sizes, key=arch_sizes.get)
    return {choosen: arch[choosen]}

def find_components(arch, component_class):
    components = set()
    for a in arch:
        if component_class in arch[a]:
            components.update(arch[a][component_class])
    return components

def contains_component(model, component, prefixed = None):
    model_keys = set([(k, tensor_shape(k, model[k])) for k in model])

    allowed = False
    if prefixed == None: #prefixed or unprefixed
        allowed = get_prefixed_keys(component).issubset(model_keys)
        allowed = allowed or COMPONENTS[component]["keys"].issubset(model_keys)
    elif prefixed == True:
        allowed = get_prefixed_keys(component).issubset(model_keys)
    elif prefixed == False:
        allowed = COMPONENTS[component]["keys"].issubset(model_keys)

    return allowed

def get_allowed_keys(arch, allowed_classes=None):
    # get all allowed keys
    allowed = set()
    for a in arch:
        if allowed_classes == None:
            allowed.update(ARCHITECTURES[a]["required"])
            allowed.update(ARCHITECTURES[a]["optional"])
        prefixed = ARCHITECTURES[a]["prefixed"]
        for clss in arch[a]:
            if allowed_classes == None or clss in allowed_classes:
                for comp in arch[a][clss]:
                    comp_keys = COMPONENTS[comp]["keys"]
                    if prefixed:
                        comp_keys = get_prefixed_keys(comp)
                    allowed.update(comp_keys)
    return allowed

def fix_model(model, fix_clip=False):
    # fix NAI nonsense
    nai_keys = {
        'cond_stage_model.transformer.embeddings.': 'cond_stage_model.transformer.text_model.embeddings.',
        'cond_stage_model.transformer.encoder.': 'cond_stage_model.transformer.text_model.encoder.',
        'cond_stage_model.transformer.final_layer_norm.': 'cond_stage_model.transformer.text_model.final_layer_norm.'
    }
    renamed = []
    for k in list(model.keys()):
        for r in nai_keys:
            if type(k) == str and k.startswith(r):
                kk = k.replace(r, nai_keys[r])
                renamed += [(k,kk)]
                model[kk] = model[k]
                del model[k]
                break
    
    # fix merging nonsense
    i = "cond_stage_model.transformer.text_model.embeddings.position_ids"
    broken = []
    if i in model:
        correct = torch.Tensor([list(range(77))]).to(torch.int64)
        current = model[i].to(torch.int64)

        broken = correct.ne(current)
        broken = [i for i in range(77) if broken[0][i]]

        if fix_clip:
            # actually fix the ids
            model[i] = correct
        else:
            # ensure fp16 looks the same as fp32
            model[i] = current

    return renamed, broken

def fix_ema(model):
    # turns UNET-v1-EMA into UNET-v1-SD
    # but only when in component form (unprefixed)

    # example keys
    # EMA = model_ema.diffusion_modeloutput_blocks91transformer_blocks0norm3weight
    # SD  = model.diffusion_model.output_blocks9.1.transformer_blocks.0.norm3.weight

    normal = COMPONENTS["UNET-v1-SD"]["keys"]
    for k, _ in normal:
        kk = k.replace(".", "")
        if kk in model:
            model[k] = model[kk]
            del model[kk]

def compute_metric(model, arch=None):
    def tensor_metric(t):
        t = t.to(torch.float16).to(torch.float32)
        return torch.sum(torch.sigmoid(t)-0.5)

    if arch == None:
        arch = inspect_model(model)

    unet_keys = get_allowed_keys(arch, ["UNET-v1", "UNET-v1-UP", "UNET-v1-DOWN", "UNET-v1-Pix2Pix", "UNET-v2", "UNET-v2-Depth", "UNET-v2-Refiner", "UNET-v3-MMDIT", "UNET-XL", "UNET-XL-UP", "UNET-XL-DOWN", "UNET-XL-A-MAIN", "UNET-XL-B-Inpainting", "UNET-XL-B-SD"])
    vae_keys = get_allowed_keys(arch, ["VAE-v1", "SD-vX-VAE", "VAE-vX-S", "VAE-vX-D", "VAE-v3"])
    clip_keys = get_allowed_keys(arch, ["CLIP-v1", "CLIP-v2", "CLIP-XL-AUX", "CLIP-v3-L"])

    unet, vae, clip = 0, 0, 0

    is_clip_v1 = "CLIP-v1" in next(iter(arch.values())) or "CLIP-XL-AUX" in next(iter(arch.values())) or "CLIP-v3-L" in next(iter(arch.values()))

    for k in model:
        kk = (k, tensor_shape(k, model[k]))

        if kk in unet_keys:
            unet += tensor_metric(model[k])

        if kk in vae_keys:
            if "encoder." in k or "decoder." in k:
                vae += tensor_metric(model[k])

        if kk in clip_keys:
            if "mlp." in k and not ".23." in k:
                clip += tensor_metric(model[k])

    b_unet, b_vae, b_clip = -6131.5400, 17870.7051, -2097.8596 if is_clip_v1 else -8757.5630
    k_unet, k_vae, k_clip = 10000, 10000, 1000000 if is_clip_v1 else 10000

    r = 10000

    n_unet = int(abs(unet/b_unet - 1) * k_unet)
    n_vae = int(abs(vae/b_vae - 1) * k_vae)
    n_clip = int(abs(clip/b_clip - 1) * k_clip)

    while n_unet >= r:
        n_unet -= r//2
    
    while n_vae >= r:
        n_vae -= r//2

    while n_clip >= r:
        n_clip -= r//2

    s_unet = f"{n_unet:04}" if unet != 0 else "----"
    s_vae = f"{n_vae:04}" if vae != 0 else "----"
    s_clip = f"{n_clip:04}" if clip != 0 else "----"

    n_unet = None if unet == 0 else n_unet
    n_vae = None if vae == 0 else n_vae
    n_clip = None if clip == 0 else n_clip
    
    return s_unet+"/"+s_vae+"/"+s_clip, (n_unet, n_vae, n_clip)

def load(file):
    model = {}
    metadata = {}

    if file.endswith(".safetensors") or file.endswith(".st"):
        model = safetensors.torch.load_file(file, device="cpu")
    else:
        model = torch.load(file, map_location="cpu")
        if not model:
            return {}, {}
        if 'state_dict' in model:
            for k in model:
                if k != 'state_dict':
                    metadata[k] = model[k]
            model = model['state_dict']

    return model, metadata

def save(model, metadata, file):
    if file.endswith(".safetensors"):
        safetensors.torch.save_file(model, file)
        return
    else:
        out = metadata
        out['state_dict'] = model
        torch.save(out, file)

def prune_model(model, arch, keep_ema, dont_half):
    allowed = get_allowed_keys(arch)
    for k in list(model.keys()):
        kk = (k, tensor_shape(k, model[k]))
        keep = False
        if kk in allowed:
            keep = True
        if k.startswith(EMA_PREFIX) and keep_ema:
            keep = True
        if not keep:
            del model[k]
            continue
        if type(model[k]) == torch.Tensor:
            if dont_half and model[k].dtype in {torch.float16, torch.float64, torch.bfloat16}:
                model[k] = model[k].to(torch.float32)
            if not dont_half and model[k].dtype in {torch.float32, torch.float64, torch.bfloat16}:
                model[k] = model[k].to(torch.float16)

def extract_component(model, component, prefixed=None):
    prefix = COMPONENTS[component]["prefix"]
    allowed = set()
    if prefixed != True:
        allowed = allowed.union(COMPONENTS[component]["keys"])
    if prefixed != False:
        allowed = allowed.union(get_prefixed_keys(component))

    for k in list(model.keys()):
        z = tensor_shape(k, model[k])
        if (k, z) in allowed:
            if k.startswith(prefix):
                kk = k.replace(prefix,"")
                if kk != k:
                    model[kk] = model[k]
                    del model[k]
        else:
            del model[k]

def replace_component(target, target_arch, source, source_component):
    if not COMPONENT_CLASS[source_component] in ARCHITECTURES[target_arch]["classes"]:
        raise ValueError(f"{target_arch} cannot contain {source_component}!")

    # get component for class
    prefix = COMPONENTS[source_component]["prefix"]
    component_keys = COMPONENTS[source_component]["keys"]

    # find out if we should prefix the component
    is_prefixed = ARCHITECTURES[target_arch]["prefixed"]

    for k in list(source.keys()):
        src_z = tensor_shape(k, source[k])
        src_k = k[len(prefix):] if k.startswith(prefix) else k
        dst_k = prefix + k if is_prefixed else k
        if (src_k, src_z) in component_keys:
            target[dst_k] = source[k]

def delete_class(model, model_arch, component_class):
    keys = set([(k, tensor_shape(k, model[k])) for k in model])
    prefixed = ARCHITECTURES[model_arch]["prefixed"]

    for name, component in COMPONENTS.items():
        if COMPONENT_CLASS[name] != component_class:
            continue
        component_keys = component["keys"] if not prefixed else get_prefixed_keys(name)
        for k in component_keys:
            if k in keys:
                del model[k[0]]
                keys.remove(k)

def log(model, file):
    keys = []
    for k in model:
        size = str(list(model[k].shape))
        keys += [f"{k},{size}"]
    keys.sort()
    out = "\n".join(keys)
    with open(file, "w") as f:
        f.write(out)

if __name__ == '__main__':
    load_components("components")

    for l in ["instruct-pix2pix-00-22000.safetensors"]:
        a, _ = load(l)
        for k in sorted(list(a.keys())):
            print(k, tensor_shape(k, a[k]))
