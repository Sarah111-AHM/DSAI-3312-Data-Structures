# main.py
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich import print as rprint

import utils
import config
from text_processor import TextProcessor
from features.autocomplete import AutocompleteFeature
from features.prediction import NextWordPredictionFeature
from features.spell import SpellSuggestionFeature
from features.sentiment import SentimentFeature

console = Console()

def load_text_interactive() -> str:
    """تطلب من المستخدم إدخال النص (مباشر أو ملف) وتعيد النص الخام."""
    console.print(Panel.fit("📄 Smart Text Analyzer", style="bold blue"))
    while True:
        choice = Prompt.ask(
            "Load text from [f]ile or enter [d]irectly?",
            choices=["f", "d"]
        )
        if choice == "f":
            file_path = Prompt.ask("Enter file path")
            path = Path(file_path)
            if not path.exists():
                console.print("[red]File not found.[/red]")
                continue
            try:
                raw = utils.load_file(path)
                console.print(f"[green]Loaded {len(raw)} characters from file.[/green]")
                return raw
            except Exception as e:
                console.print(f"[red]Error reading file: {e}[/red]")
        else:
            console.print("Enter your text (type '$$END$$' on a new line to finish):")
            lines = []
            while True:
                line = input()
                if line.strip() == "$$END$$":
                    break
                lines.append(line)
            return "\n".join(lines)

def display_menu():
    console.print("\n[bold cyan]--- Main Menu ---[/bold cyan]")
    menu_items = [
        "1. Word Statistics",
        "2. Character Statistics",
        "3. Search Word",
        "4. Replace Word",
        "5. Autocomplete (prefix)",
        "6. Next Word Prediction",
        "7. Spell Suggestion",
        "8. Sentiment Analysis",
        "0. Exit"
    ]
    for item in menu_items:
        console.print(item)
    return Prompt.ask("Choose an option", choices=[str(i) for i in range(9)])

def main():
    raw_text = load_text_interactive()
    processor = TextProcessor(raw_text)

    # بناء الميزات الذكية
    autocomplete = AutocompleteFeature(processor.unique_words)
    predictor = NextWordPredictionFeature(processor.words)
    spell = SpellSuggestionFeature(processor.unique_words)
    sentiment = SentimentFeature(config.SENTIMENT_LEXICON_PATH)

    while True:
        choice = display_menu()

        if choice == "0":
            console.print("[bold green]Goodbye![/bold green]")
            break

        elif choice == "1":  # Word Statistics
            total, unique = processor.get_word_stats()
            console.print(f"\n[underline]Word Statistics[/underline]")
            console.print(f"Total words: {total}")
            console.print(f"Unique words: {unique}")
            top_n = Prompt.ask("Show top N frequent words? (Enter number, or leave blank to skip)", default="")
            if top_n.isdigit():
                top = processor.get_top_words(int(top_n))
                table = Table(title=f"Top {top_n} Words")
                table.add_column("Word", style="cyan")
                table.add_column("Frequency", style="magenta")
                for word, count in top:
                    table.add_row(word, str(count))
                console.print(table)

        elif choice == "2":  # Character Statistics
            chars = processor.get_char_stats()
            total = sum(chars.values())
            console.print(f"\n[underline]Character Statistics[/underline]")
            console.print(f"Total characters (no spaces): {total}")
            table = Table(title="Character Frequencies")
            table.add_column("Character", style="cyan")
            table.add_column("Count", style="magenta")
            for ch, count in sorted(chars.items()):
                table.add_row(repr(ch), str(count))
            console.print(table)

        elif choice == "3":  # Search Word
            word = Prompt.ask("Enter word to search")
            results = processor.search_word(word)
            if results:
                console.print(f"Found '{word}' in {len(results)} positions:")
                for sent, wpos in results:
                    console.print(f"  Sentence {sent}, word #{wpos}")
            else:
                console.print("[yellow]Word not found.[/yellow]")

        elif choice == "4":  # Replace Word
            old = Prompt.ask("Word to replace")
            new = Prompt.ask("Replace with")
            if Confirm.ask(f"Replace all occurrences of '{old}' with '{new}'?"):
                if processor.replace_word(old, new):
                    console.print("[green]Replacement successful.[/green]")
                    # تحديث الميزات الذكية (أعد بناءها)
                    autocomplete = AutocompleteFeature(processor.unique_words)
                    predictor = NextWordPredictionFeature(processor.words)
                    spell = SpellSuggestionFeature(processor.unique_words)
                else:
                    console.print("[red]Word not found in text.[/red]")
            else:
                console.print("[yellow]Cancelled.[/yellow]")

        elif choice == "5":  # Autocomplete
            prefix = Prompt.ask("Enter prefix")
            suggestions = autocomplete.get_suggestions(prefix)
            if suggestions:
                console.print("Suggestions: " + ", ".join(suggestions))
            else:
                console.print("[yellow]No suggestions.[/yellow]")

        elif choice == "6":  # Next Word Prediction
            word = Prompt.ask("Enter a word")
            predictions = predictor.predict(word)
            if predictions:
                console.print("Next word probabilities:")
                for w, count in predictions:
                    console.print(f"  {w} (seen {count} times)")
            else:
                console.print("[yellow]No predictions.[/yellow]")

        elif choice == "7":  # Spell Suggestion
            word = Prompt.ask("Enter word to check")
            suggestions = spell.suggest(word)
            if suggestions:
                console.print("Did you mean: " + ", ".join(suggestions))
            else:
                console.print("[green]Word is correct (or no suggestions).[/green]")

        elif choice == "8":  # Sentiment
            sentence = Prompt.ask("Enter a sentence (or leave empty for full text)", default="")
            if not sentence:
                text_to_analyze = processor.clean_text
            else:
                text_to_analyze = sentence
            mood = sentiment.analyze(text_to_analyze)
            console.print(f"Sentiment: [bold]{mood.upper()}[/bold]")

        else:
            console.print("[red]Invalid choice.[/red]")

        input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted. Exiting...[/yellow]")
        sys.exit(0)
