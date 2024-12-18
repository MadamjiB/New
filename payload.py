import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Function to generate payload with exactly two '\x00' bytes
def generate_payloads(count, length):
    payloads = []
    for _ in range(count):
        # Generate a list of random bytes
        payload = [f"\\x{random.randint(1, 255):02x}" for _ in range(length - 2)]
        
        # Add exactly two '\x00' bytes
        payload.extend(["\\x00", "\\x00"])
        
        # Shuffle the list to randomize positions of '\x00' bytes
        random.shuffle(payload)
        
        # Join the payload into a string and add quotation marks
        payloads.append(f'"{"".join(payload)}"')
    
    return payloads

# Command handler for /generate
async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Check if user gave enough arguments
        if len(context.args) < 2:
            raise ValueError("Insufficient arguments.")

        # Parse the arguments
        count = int(context.args[0])  # Number of payloads
        length = int(context.args[1])  # Length of each payload in bytes

        # Validate inputs
        if count <= 0 or length <= 2:  # Length must be greater than 2 to fit two '\x00' bytes
            await update.message.reply_text("Both count and length must be positive numbers, and length must be greater than 2.")
            return

        # Generate payloads
        payloads = generate_payloads(count, length)
        
        # Add comma after each payload except the last one
        formatted_payloads = ",\n".join(payloads) + ","

        # Send payloads to user
        response_message = f"**Generated Payloads:**\n\n```\n{formatted_payloads}\n```"
        await update.message.reply_text(response_message, parse_mode='Markdown')

    except (IndexError, ValueError):
        await update.message.reply_text(
            "Invalid command format!\nUsage: `/generate <count> <length>`\nExample: `/generate 5 10`",
            parse_mode='Markdown'
        )

# Main function to run the bot
def main():
    BOT_TOKEN = "7708746499:AAGaY9DXwXsgss7vZCLOxIO-uTRiiGYj5NU"  # Replace with your bot's token
    
    # Initialize bot application
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add command handler for /generate
    app.add_handler(CommandHandler("generate", generate))

    # Start bot
    print("Bot is running... Press CTRL+C to stop.")
    app.run_polling()

if __name__ == "__main__":
    main()
