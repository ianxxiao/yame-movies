from helper.data_processing import get_data
import argparse
import logging

# Setup Argument Parser
parser = argparse.ArgumentParser()
parser.add_argument('--sample', type=float, default=1.0,
                    help='example: 0.01. default to 1')
parser.add_argument('--full', type=bool, default=False,
                   help='process the full movie dataset?')
args = parser.parse_args()


def main():

    # This is a one time pre-processing workflow to get YouTube links
    logging.info(f"batch process {args.sample*100} % of the data ...")
    final_movie_df, final_rating_df = get_data(sample_frac=args.sample)
    final_movie_df.to_csv("./data/final_movie_df.csv")
    final_rating_df.to_csv("./data/final_rating_df.csv")


if __name__ == '__main__':
    main()
