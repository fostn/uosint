
# uosint
Uosint is an Instagram OSINT (Open-Source Intelligence) tool for gathering valuable insights and information from Instagram profiles, posts, and comments. With Uosint, you can extract sensitive data, analyze user activities, and leverage the power of Chat GPT AI to perform advanced data analysis.

# Features

- Check for sensitive comments
- Get followers of a target username
- Get users that a target username is following
- Get information about a target username
- Fetch posts of a target username
- Get comments on the posts of a target username
- Download posts of a target username
- Download stories of a target username
- Extract email addresses from followers
- Extract email addresses from users that a target username is following
- Extract phone numbers from followers
- Extract phone numbers from users that a target username is following
- Detect and analyze text in the images of the target username stories
# Installation

1. Clone the repository:
   ```shell
   git clone https://github.com/fostn/uosint.git
   ```
2. Navigate to the project directory:
  ```shell
  cd uosint
  ```
3. After entering your Instagram account information Install the project dependencies:

 ```shell
 python setup.py install
 ```
 This will install all the required dependencies for Uosint.
# Configuration
Before using Uosint, make sure to configure your credentials.

Open the config/credentials.ini file and enter your Instagram account credentials.

## Token

After successful login, the token will be generated and automatically saved in the `config/token.ini` file. You don't need to manually edit this file. The token is used for authentication purposes and enables access to the relevant services.

**Note:** It is essential to keep your credentials and token secure and not share them publicly .
# Usage

To use Uosint, execute the following command:
```shell
uosint <command> <username>
```
Replace <command> with one of the available commands from the features list below and <username> with the target Instagram username.
## Available commands
- `sensitive`: Search for sensitive Data
    - Option: `-c`
    - Description: Get sensitive data from user comments

- `followers`: Get the followers of the target username
- `following`: Get the users that the target username is following
- `info`: Get the information of the target username
- `posts`: Get the posts of the target username
- `comments`: Get the comments on the posts of the target username
- `fwersemail`: Extract email addresses from the followers' bio of the target username
- `fwingsemail`: Extract email addresses from the users' bio that the target username is following
- `fwersnumber`: Extract phone numbers from the followers' bio of the target username
- `fwingsnumber`: Extract phone numbers from the users' bio that the target username is following
- `d-posts`: Download the posts of the target username
- `d-stories`: Download the stories of the target username
- `detect`: Detect and analyze text in the images of the target username stories
    - Option: `-i`
    - Description: Detect and analysis text in the images of the stories
   - Option: `-s`
    - Description: Detect and analysis text in the stories

For example, to check for sensitive comments, use the following command
```shell
  uosint sensitive -c <username>

 ```
 
