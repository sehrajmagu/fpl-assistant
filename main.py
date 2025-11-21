from src.fpl_data import get_top_players

def main():
    df = get_top_players()
    print("\nTop Players in FPL Right Now\n")
    print(df.to_string(index=False))

if __name__ == "__main__":
    main()
