#!/usr/bin/python3
# As an example, let’s convert the text "a sleepy ridgeback dog" into an embedding. 
# For purposes of brevity, we have cropped the full embedding result which can be found here.
# python generate.py --text "a sleepy ridgeback dog"
# [0.5736801028251648, 0.2516217529773712, ...,  -0.6825592517852783]

import argparse
from PIL import Image
import clip
import torch

if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		prog='generate',
		description='Generate CLIP embeddings for images or text')
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument('--text', required=False)
	group.add_argument('--image', required=False)
	parser.add_argument('--limit', default=1)
	parser.add_argument('--table', default='laion_1m')
	args = parser.parse_args()
	device = "cuda" if torch.cuda.is_available() else "cpu"
	print(f"using {device}")
	device = torch.device(device)
	model, preprocess = clip.load("ViT-L/14")
	model.to(device)
	images = []
	if args.text:
		print(f"Gathering embeddings for {args.text}")
		inputs = clip.tokenize(args.text)
		with torch.no_grad():
			print(model.encode_text(inputs)[0].tolist())
	elif args.image:
		print(f"Gathering embeddings for {args.image}")
		image = preprocess(Image.open(args.image)).unsqueeze(0).to(device)
		with torch.no_grad():
			print(model.encode_image(image)[0].tolist())