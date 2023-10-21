from diffusers import DiffusionPipeline
import torch

class SDXLAgent():
    def __init__(self, n_steps = 40, high_noise_frac = 0.8, offload_mode=False):
        self.MODELS = ("base", "refiner")
        # Define how many steps and what % of steps to be run on each experts (80/20) here
        self.n_steps = n_steps
        self.high_noise_frac = high_noise_frac
        self.offload_mode = offload_mode
        self.loaded_model = None

        # load both base & refiner
        self.base = DiffusionPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, variant="fp16", use_safetensors=True
        )
        self.refiner = DiffusionPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-refiner-1.0",
            text_encoder_2 = self.base.text_encoder_2,
            vae = self.base.vae,
            torch_dtype=torch.float16,
            use_safetensors=True,
            variant="fp16",
        )
        self.on_init()
       

    def on_init(self):
        self.load_model(self.MODELS[0])

    def offload_model(self, name):
        print(f"Warning : Fail to load {name} model in cuda GPU")
        torch.cuda.empty_cache()
        if name == "base":
            self.base.enable_model_cpu_offload()
        elif name == "refiner":
            self.refiner.enable_model_cpu_offload()

    def load_model(self, name, offload=False):
        if name in self.MODELS:
            if offload or self.offload_mode:
                self.offload_model(name)
            else:
                if name != self.loaded_model:
                    try:
                        torch.cuda.empty_cache()
                        if name == "base":
                            self.base.to("cuda")
                        elif name == "refiner":
                            self.refiner.to("cuda")
                    except:
                        self.offload_model(name)
                    self.loaded_model = name
        else:
            raise(f"wrong model name : {name}")

    def refine_image(self, prompt, image):
        refine_image = self.refiner(
            prompt = prompt,
            num_inference_steps = self.n_steps,
            denoising_start = self.high_noise_frac,
            image = image,
        ).images[0]

        return refine_image

    def create_image(self, prompt, height = 720, width = 1280, refine = True, offload=False):
        self.load_model("base", offload)
        image = self.base(
            prompt = prompt,
            height = height,
            width = width,
            num_inference_steps = self.n_steps,
            denoising_end = self.high_noise_frac,
            output_type = "latent" if refine else "",
        ).images
        if refine:
            self.load_model("refiner", offload)
            image = self.refine_image(prompt=prompt, image=image)

        return image
    
    def get_image(self, prompt, height = 720, width = 1280, refine = True, offload=False):
        try:
            image = self.create_image(
                prompt=prompt,
                height=height,
                width=width,
                refine=refine,
                offload=offload
            )
            print("fail to create image : offload mode is active")
        except:
            self.offload_mode = True
            image = self.create_image(
                prompt=prompt,
                height=height,
                width=width,
                refine=refine,
                offload=True
            )
        return image
