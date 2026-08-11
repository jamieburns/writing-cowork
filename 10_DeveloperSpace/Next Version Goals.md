
# Version 0.15 tasks - input from projects and clean
1. Add reseach and analysis folder with rules
2. Add resources folder - read only - but stop downloading things over and over
	1. Allow some to be stashed and some commited. - how to manage?
3. Look at possible other skill consolidate.
4. ==**Develop version update process.**==
5. Roll out to current projects.

# Version 0.16. -memory and role management
1. Roll cowork-tools into skills or something
2. Memory management
3. Role mapping - clean and concise
4. Session start up by hook
5. Session end handoff - start handoff - cleanup - not saved.
6. Update new project standup

# Version 0.17 - Process Management
1. Better git integration? Get git on the inside
2. Better claude cowork / claude cowork cloud integration
3. Change some PM to process/skill that any one can do.
4. Easier access to consistent road map and steps
5. Better HUB
6. Kanban - HUB - Dashboard.
7. Can we move to using worktrees so concurrent activiities be managed better?
8. Generate guide for usage?
9. **Rollout to new Project "B"**

# Version 0.18 - REVIEW PROCESS DEV/Update
1. Review Subagent Developement - Expansion in project.
2. Get inputs from each project.
3. Develop way to start and manage runets offline

# Verision 0.19 - Last Things
1. PRoduction - see below
2. Get feedback from users
3. TBD

# Version 0.2 - Release 
1. Do I make public?
2. Is there something out there better?
# Things that need to be addressed
## Clean Up Development
1. ~~Move cowork-tools to live in plugin/skills (possible - possibly populate files with initial skill or something - maybe have )~~
2. ~~Review skill list - do we need to cull~~
3. ~~Optimized roll def - simple links from claude md or memory~~

## Process Development
1. Change some PM to process/skill that any one can do.
2. Easier access to consistent road map and steps
3. Better HUB
4. Kanban - HUB - Dashboard.
5. Production Development Cycle (art, graphics, epub, print, pdf, Words)
6. 

## ~~Review Development~~
1. ~~Take process development from current projects~~

## ~~Acquire Inputs from Projects.~~

## ~~Subagent Development for Reviews in plugin~~

## ~~Generate Hooks for session startup~~

# Manage old chats
1. Archive Chats marked complete after 2 days - scheduled job
2. Archived chat management
	1. list archive
	2. search archive
	3. delete - bad chat - marking bad chats - with norification if possible.


Yes, a community-made skill called ==[unarchive-cowork](https://lobehub.com/skills/ericpardee-claude-files-unarchive-cowork)== handles this. You can find it on marketplaces like LobeHub or [Skillhub](https://www.youtube.com/watch?v=HTu1OGWAn5w). [1, 2] 

Alternatively, because a Claude Cowork skill is simply a folder containing a `skill.md` file, you can create your own custom skill inside your Cowork directory to automate this. [3, 4] 

---

## Custom Skill Implementation

Create a folder named `manage-archived-chats` inside your Cowork environment. Inside it, save a file named `skill.md` with the following template: [4, 5, 6] 

```markdown
# Manage Archived Chats
Skill to list and unarchive hidden local agent mode chat sessions.

## 1. List Archived Chats
When asked to list archived chats, parse the `local-agent-mode-sessions` directory. Read each `uuid.json` file. Filter and display files where `"isArchived": true`. Support string or keyword search criteria within the chat titles or file names.

## 2. Unarchive Chats
When asked to unarchive a chat by name, search for matching session JSON titles. Support wildcards (e.g., `Project*`). For all matches, modify the metadata string from `"isArchived": true` to `"isArchived": false`. Instruct the user to restart Claude to apply changes.
```

---

💡 Next steps:

- Would you like me to generate the exact terminal commands this skill will execute under the hood?
- I can show you how to toggle the skill on in your Cowork capabilities panel. [2, 4, 7] 

- generate terminal commands
- how to toggle skill on

  

[1] [https://lobehub.com](https://lobehub.com/skills/ericpardee-claude-files-unarchive-cowork)

[2] [https://www.youtube.com](https://www.youtube.com/watch?v=HTu1OGWAn5w&t=618)

[3] [https://platform.claude.com](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)

[4] [https://www.youtube.com](https://www.youtube.com/watch?v=mS5ojqQ7zzw&t=678)

[5] [https://www.youtube.com](https://www.youtube.com/watch?v=kfjgmhSn0U8)

[6] [https://agentfactory.panaversity.org](https://agentfactory.panaversity.org/docs/General-Agents-Foundations/general-agents/skills-exercises)

[7] [https://www.facebook.com](https://www.facebook.com/groups/claudeaicommunity/posts/1240075048159660/)