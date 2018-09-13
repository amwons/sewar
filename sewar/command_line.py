import argparse
import sewar
from PIL import Image
import numpy as np
import re
import ast

metrics = dict(mse=sewar.full_ref.mse,
				rmse=sewar.full_ref.rmse,
				psnr=sewar.full_ref.psnr,
				rmse_sw=sewar.full_ref.rmse_sw,
				uqi=sewar.full_ref.uqi,
				ssim=sewar.full_ref.ssim,
				ergas=sewar.full_ref.ergas,
				scc=sewar.full_ref.scc,
				rase=sewar.full_ref.rase,
				sam=sewar.full_ref.sam,
				msssim=sewar.full_ref.msssim,
				vifp=sewar.full_ref.vifp,
				d_lambda=sewar.no_ref.d_lambda,
				d_s=sewar.no_ref.d_s,
				qnr=sewar.no_ref.qnr)

desc = """Description: command-line interface to sewar: image quality package"""
epilog = """You can add any extra argument needed for the function (check documentation for more info).
			Example: passing window size (ws) would be as [-ws 11]
		"""


def str_to_array(str):
	pattern = r'''# Match (mandatory) whitespace between...
			(?<=\]) # ] and
			\s+
			(?= \[) # [, or
			|
			(?<=[^\[\]\s]) 
			\s+
			(?= [^\[\]\s]) # two non-bracket non-whitespace characters
			'''
	return np.array(ast.literal_eval(str))

extra_args = dict(ws=int,
				MAX=float,
				K1=float,
				K2=float,
				r=int,
				fltr=str_to_array,
				weights=str_to_array,
				sigma_nsq=float)

def main():	
	parser = argparse.ArgumentParser(prog='sewar',description=desc,epilog=epilog)
	parser.add_argument('metric',
					choices=metrics.keys(),
					help='metric to calculate')
	parser.add_argument('GT', help='first (reference) image path')
	parser.add_argument('P', help='second (query) image path')

	args,unknown = parser.parse_known_args()

	kwargs = dict()
	for i in range(0,len(unknown),2):
		if unknown[i][0] != '-':
			raise Exception('wrong supplied argument "%s". all arguments should start with "-"'%(unknown[i]))
		key =unknown[i][1:]
		val =unknown[i+1]
		kwargs[key] = extra_args[key](val)

	gt = np.asarray(Image.open(args.GT))
	p = np.asarray(Image.open(args.P))
	print(args.metric,":",metrics[args.metric](gt,p,**kwargs))