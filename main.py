import argparse
from src.uosint import Uosint
from src.api import InstagramAPI

def main():
    # Create the command-line argument parser
    parser = argparse.ArgumentParser(description='Uosint Command Line Tool')

    subparsers = parser.add_subparsers(dest='command', help='Specify the command to execute.')

    # Create a parser for the "sensitive" command
    sensitive_parser = subparsers.add_parser('sensitive', help='Check for sensitive comments')
    sensitive_parser.add_argument('-c', '--get_sensitive_comments', action='store_true', help='Get sensitive comments')
    

    # Add descriptions for other commands
    subparsers.add_parser('followers', help='Get the followers of the target username')
    subparsers.add_parser('following', help='Get the users that the target username is following')
    subparsers.add_parser('info', help='Get the information of the target username')
    subparsers.add_parser('posts', help='Get the posts of the target username')
    subparsers.add_parser('comments', help='Get the comments on the posts of the target username')
    subparsers.add_parser('fwersemail', help='Extract email addresses from the followers of the target username')
    subparsers.add_parser('fwingsemail', help='Extract email addresses from the users that the target username is following')
    subparsers.add_parser('fwersnumber', help='Extract phone numbers from the followers of the target username')
    subparsers.add_parser('fwingsnumber', help='Extract phone numbers from the users that the target username is following')
    subparsers.add_parser('pocomments', help='Get the comments on the posts of the target username')
    parser.add_argument('username', help='Specify the target username')
    # Parse the command-line arguments
    args = parser.parse_args()
    uosint = Uosint()

    # Execute the corresponding method based on the command
    if args.command == 'followers':
        uosint.get_followers(args.username)
    elif args.command == 'following':
        uosint.get_following(args.username)
    elif args.command == 'info':
        uosint.get_user_info(args.username)
    elif args.command == 'posts':
        uosint.get_posts(args.username)
    elif args.command == 'comments':
        uosint.get_comments(args.username)
    elif args.command == 'fwingsnumber':
        uosint.get_fwingsnumber(args.username)
    elif args.command == 'fwersnumber':
        uosint.get_fwersnumber(args.username)
    elif args.command == 'fwersemail':
        uosint.get_fwersemail(args.username)
    elif args.command == 'fwingsemail':
        uosint.get_fwingsemail(args.username)
    elif args.command == 'pocomments':
        uosint.get_posts_comments(args.username)
    elif args.command == 'sensitive':
        if args.get_sensitive_comments:
            uosint.get_sensitive_comments(args.username)
        else:
            print("No option specified. Use -h or --help for available options.")
    else:
        print("Command not found. Use -h or --help for available commands.")

if __name__ == '__main__':
    main()
