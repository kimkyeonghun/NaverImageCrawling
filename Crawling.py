import argparse

from NaverImageCrawling import NaverImageCrawling

images =NaverImageCrawling.NaverImageCrawling()

parser = argparse.ArgumentParser()
parser.add_argument('--keyword', type=str, required=True)
parser.add_argument('--n', type=int, required=True)
parser.add_argument('--path', type=str, default='')
args = parser.parse_args()

images.download_image(args.keyword, args.n, args.path)