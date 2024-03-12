from datetime import datetime
from mongodb_operations import get_duplicate_reference_ids
from excel_operations import export_to_excel
from email_operations import send_email_with_attachment

def main():
    # Fetch duplicate reference IDs from MongoDB
    aggregation_results = get_duplicate_reference_ids()

    # Export duplicate reference IDs to Excel
    excel_filepath = export_to_excel(aggregation_results)

    # Sending Email with Attachment
    sender_email = ""  # Update with your sender email
    receiver_email = ""
    cc_email = "m"  # Update with receiver's email

    today_date = datetime.now().strftime("%Y-%m-%d")
    subject = f"Duplicate Records In Planning Data Collections on {today_date}"

    message_text = (
        "Hi Team,\n\n"
        "I hope this mail finds you well.\n\n"
        "These are the duplicate records in planning data collections for a better output we need to delete these records from our backend collections.\n\n"
        "Best regards,\n"
        "Fazan"
    )

    send_email_with_attachment(sender_email, receiver_email, cc_email, subject, message_text, excel_filepath)

if __name__ == "__main__":
    main()
