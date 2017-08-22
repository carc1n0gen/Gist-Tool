# Gist-Tool
Python script for making gists from the command line

## Environment Variables

```
export GH_USERNAME=<Github Username>
export GH_GIST_TOKEN=<Personal Access Token>
export GH_API_URL=https://api.github.com/v3 # This can be customized for use with an onprem instance of github
```

## Usage

Command                                           | Explanation
------------------------------------------------- | -------------------------------------------------------------------------
`cat <file> \| gist.py`                            | Generate a gist with a name and description set to the current date/time.
`cat <file> \| gist.py -n <name> -d <description>` | Generate a gist with a custom file name and description
`cat <file> \| gist.py -p`                         | Generate a gist and flag it as private


## Security Considerations

It is recommended that the personal access token that you generate for use with this tool only has access to your gists.


