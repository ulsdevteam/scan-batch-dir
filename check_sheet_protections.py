#!/usr/bin/python3.12
"""
Standalone diagnostic: list protected ranges/sheets on a Google Sheet,
and check whether a given service account email is allowed to bypass them.

Usage:
    python3 check_sheet_protections.py \
        --spreadsheet-id 1_nnBcCt4MPaAzaXqvAVD2pMv8AX9wPj8BBfgI-05Ri8 \
        --creds /path/to/configuration.json
"""

import argparse
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build


def connect(credentials_file):
    scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    creds = service_account.Credentials.from_service_account_file(
        credentials_file, scopes=scopes
    )
    return build('sheets', 'v4', credentials=creds)


def get_service_account_email(credentials_file):
    with open(credentials_file) as f:
        data = json.load(f)
    return data.get('client_email', 'UNKNOWN')


def describe_range(rng):
    if not rng:
        return "ENTIRE SHEET (no bounds set)"
    parts = []
    if 'startRowIndex' in rng or 'endRowIndex' in rng:
        parts.append(f"rows {rng.get('startRowIndex', '0')}-{rng.get('endRowIndex', 'end')}")
    if 'startColumnIndex' in rng or 'endColumnIndex' in rng:
        parts.append(f"cols {rng.get('startColumnIndex', '0')}-{rng.get('endColumnIndex', 'end')}")
    return ", ".join(parts) if parts else "ENTIRE SHEET (no bounds set)"


def main():
    parser = argparse.ArgumentParser(description="Check Google Sheet protected ranges.")
    parser.add_argument('--spreadsheet-id', required=True)
    parser.add_argument('--creds', required=True, help="Path to service account credentials JSON.")
    args = parser.parse_args()

    sa_email = get_service_account_email(args.creds)
    print(f"Service account: {sa_email}\n")

    service = connect(args.creds)
    result = service.spreadsheets().get(
        spreadsheetId=args.spreadsheet_id,
        fields="sheets(properties(sheetId,title),protectedRanges)"
    ).execute()

    found_any = False
    for sheet in result.get('sheets', []):
        title = sheet['properties']['title']
        for pr in sheet.get('protectedRanges', []):
            found_any = True
            editors = pr.get('editors', {})
            editor_users = editors.get('users', [])
            domain_can_edit = editors.get('domainUsersCanEdit', False)

            print(f"Sheet/Tab:     {title}")
            print(f"Description:   {pr.get('description', '(none)')}")
            print(f"Scope:         {describe_range(pr.get('range'))}")
            print(f"Warning only:  {pr.get('warningOnly', False)}")
            print(f"Editor list:   {editor_users if editor_users else '(empty/not visible)'}")
            print(f"Domain can edit: {domain_can_edit}")

            if pr.get('warningOnly', False):
                print("  -> Warning-only: this protection would NOT block the service account's writes.")
            elif sa_email in editor_users:
                print(f"  -> Service account IS listed as an allowed editor for this protection.")
            else:
                print(f"  -> Service account is NOT listed. THIS PROTECTION IS LIKELY BLOCKING WRITES.")
            print()

    if not found_any:
        print("No protected ranges found on any sheet/tab in this spreadsheet.")
        print("(If writes are still failing with a 400 protection error, double check")
        print(" you're pointing at the correct spreadsheet ID / tab name, or that the")
        print(" service account even has enough access to see the protection metadata.)")


if __name__ == "__main__":
    main()