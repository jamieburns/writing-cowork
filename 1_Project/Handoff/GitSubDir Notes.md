
To host your plugin contents inside a subdirectory and pull it directly into the Claude Desktop App via GitHub, you must use a git-subdir reference block inside a root `marketplace.json` catalog. [1] 

Here are the precise step-by-step instructions to configure, push, and sync it.

---

## Step 1: Scaffold the Subdirectory Repository Structure

Organize your local Git repository so the actual plugin lives nested in a subfolder, while a marketplace catalog sits at the true repository root. [2] 

```text
your-git-repo/                 # Root of your GitHub repository
├── .claude-plugin/            # REQUIRED: Root configuration directory
│   └── marketplace.json       # The marketplace index pointing to your subdirectory
└── modules/                   
    └── my-custom-plugin/      # Your plugin subdirectory folder
        ├── .claude-plugin/
        │   └── plugin.json    # The local plugin manifest
        └── skills/
            └── core-workflow/
                └── SKILL.md   # The file containing the specific skill logic
```

## Step 2: Configure the Root `marketplace.json`

Create a `.claude-plugin/marketplace.json` file at the root of your Git repository. Use the `git-subdir` source type to point Claude directly into your specific subfolder: [1, 3] 

```json
{
  "name": "my-custom-marketplace",
  "owner": {
    "name": "Your Name",
    "email": "you@example.com"
  },
  "plugins": [
    {
      "name": "my-custom-plugin",
      "source": {
        "source": "git-subdir",
        "url": "https://github.com",
        "path": "modules/my-custom-plugin"
      },
      "version": "1.0.0",
      "description": "A workflow plugin hosted entirely in a subfolder"
    }
  ]
}
```

## Step 3: Configure the Subdirectory `plugin.json`

Create the `modules/my-custom-plugin/.claude-plugin/plugin.json` file inside your subdirectory to declare its component dependencies: [2, 4] 

```json
{
  "name": "my-custom-plugin",
  "version": "1.0.0",
  "type": "workflow",
  "skills": [
    "core-workflow"
  ]
}
```

## Step 4: Push the Subfolder Layout to GitHub

Commit your localized directory structure and push it to your GitHub remote destination: [5, 6, 7, 8] 

```bash
git add .
git commit -m "feat: implement subdirectory plugin with root git-subdir source"
git push origin main
```

## Step 5: Link the Marketplace into Claude Desktop

1. Launch the Claude Desktop App.
2. Click on the Cowork Tab at the top panel.
3. Click the Settings (Gear) Icon -> Plugins -> Add Marketplace.
4. Paste your root GitHub URL (`https://github.com`) and click Sync.
5. Claude will parse the root configuration, sparse-clone only the targeted `modules/my-custom-plugin` subfolder, and display your plugin. Click Install / `+` to activate it. [1, 9, 10, 11, 12] 

---

💡 If your repository is Private, Claude Desktop will fail to clone the subdirectory without authorization. Would you like the steps to configure an SSH Key or a GitHub Personal Access Token (PAT) in your Claude environment variables? Or would you like to review how to write slash commands (`/`) inside your subfolder plugin? [4, 13] 

- Configure Private Repository Authentication
- Add custom slash commands to the subfolder [14, 15] 

  

[1] [https://code.claude.com](https://code.claude.com/docs/en/plugin-marketplaces)

[2] [https://code.claude.com](https://code.claude.com/docs/en/plugin-marketplaces)

[3] [https://github.com](https://github.com/Turek/cowork-global-memory)

[4] [https://medium.com](https://medium.com/@automation.labs/ship-a-claude-code-plugin-as-a-zip-url-a-7-step-may-2026-build-0c570824741e)

[5] [https://www.youtube.com](https://www.youtube.com/watch?v=XI1js-SyNSY&vl=pa)

[6] [https://medium.com](https://medium.com/@tejashavirishav/20-git-commands-every-developer-should-know-df93aeaa8f78)

[7] [https://www.youtube.com](https://www.youtube.com/watch?v=CTul4wE4Aq0)

[8] [https://ecanarys.com](https://ecanarys.com/git-command-line-options/)

[9] [https://github.com](https://github.com/anthropics/financial-services)

[10] [https://github.com](https://github.com/JJenglert1/getting-started-with-claude-cowork)

[11] [https://dev.to](https://dev.to/nagell/build-your-own-claude-code-marketplace-scaffold-structure-and-auto-updates-4n3f)

[12] [https://warin.ca](https://warin.ca/dpr/git.html)

[13] [https://www.reddit.com](https://www.reddit.com/r/ClaudeCowork/comments/1t7dfii/build_you_first_ai_employee_with_claude_cowork/)

[14] [https://meta.discourse.org](https://meta.discourse.org/t/install-plugins-on-a-self-hosted-site/19157)

[15] [https://help.apiary.io](https://help.apiary.io/tools/github-integration/)