import sys,os
sys.path.append('../../../')
from utils.get_parent_path import get_parent_path
bundle_dir=get_parent_path(3)+os.sep+'model_zoo'+os.sep+'mrcnn'
sys.path.append(bundle_dir)
from mrcnn import visualize
import matplotlib.pyplot as plt
import skimage,cv2
import numpy as np

import random
import itertools
import colorsys

import numpy as np
from skimage.measure import find_contours
import matplotlib.pyplot as plt
from matplotlib import patches,  lines
from matplotlib.patches import Polygon

def random_colors(N, bright=True):
	"""
	Generate random colors.
	To get visually distinct colors, generate them in HSV space then
	convert to RGB.
	"""
	brightness = 1.0 if bright else 0.7
	hsv = [(i / N, 1, brightness) for i in range(N)]
	colors = list(map(lambda c: colorsys.hsv_to_rgb(*c), hsv))
	random.shuffle(colors)
	return colors

def get_ax(rows=1, cols=1, size=16):
	"""Return a Matplotlib Axes array to be used in
	all visualizations in the notebook. Provide a
	central point to control graph sizes.

	Adjust the size attribute to control how big to render images
	"""
	_, ax = plt.subplots(rows, cols, figsize=(size*cols, size*rows))
	return ax

def color_splash(image, mask):
	"""Apply color splash effect.
	image: RGB image [height, width, 3]
	mask: instance segmentation mask [height, width, instance count]

	Returns result image.
	"""
	# Make a grayscale copy of the image. The grayscale copy still
	# has 3 RGB channels, though.
	gray = skimage.color.gray2rgb(skimage.color.rgb2gray(image)) * 255
	# Copy color pixels from the original color image where mask is set
	if mask.shape[-1] > 0:
		# We're treating all instances as one, so collapse the mask into one layer
		mask = (np.sum(mask, -1, keepdims=True) >= 1)
		splash = np.where(mask, image, gray).astype(np.uint8)
	else:
		splash = gray.astype(np.uint8)
	return splash
def apply_mask(image, mask, color, alpha=0.5):
	"""Apply the given mask to the image.
	"""
	for c in range(3):
		image[:, :, c] = np.where(mask == 1,
								  image[:, :, c] *
								  (1 - alpha) + alpha * color[c] * 255,
								  image[:, :, c])
	return image

def display_instances(image, boxes, masks, class_ids, class_names,
					  scores=None, title="",
					  figsize=(16, 16), ax=None,
					  show_mask=True, show_bbox=True,
					  colors=None, captions=None):
	# Number of instances
	N = boxes.shape[0]
	if not N:
		print("\n*** No instances to display *** \n")
	else:
		assert boxes.shape[0] == masks.shape[-1] == class_ids.shape[0]

	# If no axis is passed, create one and automatically call show()
	auto_show = False

	if not ax:
		_, ax = plt.subplots(1, figsize=figsize)
		auto_show = True

	# Generate random colors
	colors = colors or random_colors(N)

	# Show area outside image boundaries.
	height, width = image.shape[:2]
	ax.set_ylim(height + 10, -10)
	ax.set_xlim(-10, width + 10)
	ax.axis('off')
	ax.set_title(title)

	masked_image = image.astype(np.uint32).copy()
	for i in range(N):
		color = colors[i]
	#
		# Bounding box
		if not np.any(boxes[i]):
			# Skip this instance. Has no bbox. Likely lost in image cropping.
			continue
		y1, x1, y2, x2 = boxes[i]
		if show_bbox:
			p = patches.Rectangle((x1, y1), x2 - x1, y2 - y1, linewidth=2,
								alpha=0.7, linestyle="dashed",
								edgecolor=color, facecolor='none')
			ax.add_patch(p)

		# Label
		if not captions:
			class_id = class_ids[i]
			score = scores[i] if scores is not None else None
			print(class_id)
			label = class_names[class_id]
			caption = "{} {:.3f}".format(label, score) if score else label
		else:
			caption = captions[i]
		ax.text(x1, y1 + 8, caption,
				color='w', size=11, backgroundcolor="none")

		# Mask
		mask = masks[:, :, i]
		if show_mask:
			masked_image = apply_mask(masked_image, mask, color)

		# Mask Polygon
		# Pad to ensure proper polygons for masks that touch image edges.
		padded_mask = np.zeros(
			(mask.shape[0] + 2, mask.shape[1] + 2), dtype=np.uint8)
		padded_mask[1:-1, 1:-1] = mask
		contours = find_contours(padded_mask, 0.5)
		for verts in contours:
			# Subtract the padding and flip (y, x) to (x, y)
			verts = np.fliplr(verts) - 1
			p = Polygon(verts, facecolor="none", edgecolor=color)
			ax.add_patch(p)
	cv2.imshow('img',masked_image.astype(np.uint8))
	cv2.waitKey(0)


def post_process(image,results):
	ax = get_ax(1)
	r=results[0]

	display_instances(image[0], r['rois'], r['masks'], r['class_ids'],['background','elegans'], r['scores'],title="Predictions")
	# mask=r['masks']
	# print(r['masks'])
	# print(r['scores'])
	# splash = color_splash(image[0], r['masks'])
	# cv2.imshow('img',splash)
	# cv2.waitKey(0)
		# Save output
