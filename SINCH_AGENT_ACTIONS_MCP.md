# Sinch Agent Actions MCP Proposal

## Executive summary

Sinch should expose a hosted MCP server that lets third-party AI agents and workflow platforms use Sinch as their trusted customer communication action layer.

The product is not another chatbot, campaign generator, or HubSpot messaging app. It is a standard tool interface that external agents can call to:

- choose the right channel,
- send customer messages,
- send approved templates,
- check delivery status,
- classify inbound replies,
- check message risk,
- estimate message volume and cost.

This approach lets platforms integrate with Sinch instead of requiring Sinch to build a separate full application for every platform.

## Product positioning

Product name:

> Sinch Agent Actions MCP Server

Customer-facing message:

> Give your AI agents a safe way to contact customers through SMS, WhatsApp, RCS, MMS, and other Sinch-supported channels.

Developer-facing message:

> Connect any MCP-compatible agent to Sinch messaging, delivery tracking, reply understanding, and channel intelligence.

Business goal:

> Increase Sinch messaging volume by allowing external AI agents and workflow platforms to trigger compliant, trackable, multichannel customer communications.

Primary KPI:

```text
AI-agent-triggered message volume
```

Supporting KPIs:

- active MCP-connected customers,
- active third-party workflows,
- messages sent by MCP tools,
- fallback messages,
- channel mix expansion,
- reply automation rate,
- estimated and actual Sinch revenue,
- customer business outcome, such as bookings, renewals, payments, or recovered carts.

## Architecture

```text
Third-party AI platform
Claude, n8n, enterprise agent, workflow agent, CRM agent
        |
        | MCP client connection
        v
Sinch hosted MCP server
        |
        v
Sinch Agent Actions Gateway
        |
        +--> Conversation API
        +--> Sinch Engage
        +--> SMS API
        +--> consent and opt-out policy
        +--> delivery status store
        +--> pricing and volume estimator
        +--> audit logging
        +--> webhook listener
```

### Why separate MCP server and gateway?

The MCP server should expose tools and schemas. The Agent Actions Gateway should own business logic.

MCP server responsibilities:

- expose tool definitions,
- validate tool input shape,
- authenticate MCP clients,
- resolve tenant/account context,
- call the Agent Actions Gateway,
- return structured results to the external agent.

Gateway responsibilities:

- call Sinch APIs,
- enforce consent, opt-out, quiet-hour, spend, and rate policies,
- handle approved templates,
- store message/action audit events,
- track delivery receipts,
- calculate volume and cost estimates,
- support future adapters such as OpenAPI, HubSpot actions, Salesforce actions, Zapier, or Power Automate.

This keeps the core capability reusable. MCP is the first interface, not the only possible interface.

## First release tools

Release the smallest tool set that can create measurable message volume and still be safe for enterprise customers.

### 1. `recommend_channel`

Purpose:

Recommend the primary channel and fallback channel for a given use case.

Why it matters:

This encourages customers to move from single-channel SMS usage to multichannel usage with WhatsApp, RCS, MMS, or SMS fallback.

Input:

```json
{
  "country": "US",
  "use_case": "lead_follow_up",
  "urgency": "medium",
  "sms_opt_in": true,
  "whatsapp_opt_in": true,
  "rcs_available": false,
  "customer_value": "high"
}
```

Output:

```json
{
  "primary_channel": "WHATSAPP",
  "fallback_channel": "SMS",
  "confidence": "medium",
  "reason": "WhatsApp opt-in exists and supports richer follow-up. SMS fallback improves reach if WhatsApp delivery fails."
}
```

Implementation notes:

- Start rule-based with lightweight AI explanation.
- Use country, use case, urgency, opt-in status, channel availability, and customer value.
- Keep recommendation deterministic enough for enterprise trust.

### 2. `send_message`

Purpose:

Send a one-off message through Sinch.

Input:

```json
{
  "recipient": "+14155550100",
  "body": "Acme: Your appointment is tomorrow at 2 PM. Reply C to confirm or R to reschedule.",
  "use_case": "appointment_reminder",
  "channels": ["WHATSAPP", "SMS"],
  "fallback_enabled": true,
  "external_reference": "hubspot_contact_123"
}
```

Output:

```json
{
  "message_id": "msg_123",
  "status": "queued",
  "primary_channel": "WHATSAPP",
  "fallback_channel": "SMS",
  "audit_id": "audit_456"
}
```

Implementation notes:

- Default to Conversation API for omnichannel use cases.
- Tag every send with source metadata:

```json
{
  "source": "sinch_agent_actions_mcp",
  "platform": "n8n",
  "workflow_id": "abandoned_cart_recovery",
  "external_reference": "hubspot_contact_123"
}
```

- Require stronger guardrails for bulk sends.

### 3. `send_template_message`

Purpose:

Send an approved template message, especially for WhatsApp or regulated enterprise workflows.

Input:

```json
{
  "recipient": "+14155550100",
  "template_id": "payment_reminder_v2",
  "template_parameters": {
    "first_name": "Anna",
    "amount": "$49.00",
    "due_date": "2026-06-03"
  },
  "channels": ["WHATSAPP", "SMS"],
  "fallback_enabled": true,
  "external_reference": "salesforce_case_987"
}
```

Output:

```json
{
  "message_id": "msg_124",
  "status": "queued",
  "template_id": "payment_reminder_v2",
  "primary_channel": "WHATSAPP",
  "audit_id": "audit_457"
}
```

Implementation notes:

- This should be preferred over free-form `send_message` for enterprise and marketing use cases.
- It reduces brand, compliance, and hallucination risk.
- Template availability can be scoped by Sinch account and channel.

### 4. `get_delivery_status`

Purpose:

Let the external agent check delivery state and decide the next action.

Input:

```json
{
  "message_id": "msg_123"
}
```

Output:

```json
{
  "message_id": "msg_123",
  "status": "delivered",
  "channel": "WHATSAPP",
  "delivered_at": "2026-05-31T09:00:00Z",
  "failure_reason": null
}
```

Implementation notes:

- Backed by Sinch delivery receipts and webhook ingestion.
- Status should be normalized across channels.
- Later, add `wait_for_delivery_status` for platforms that support long-running tool calls.

### 5. `classify_reply`

Purpose:

Classify inbound customer replies so third-party workflows can branch.

Input:

```json
{
  "incoming_message": "Yes please book me for tomorrow",
  "conversation_context": "lead_follow_up",
  "language": "en"
}
```

Output:

```json
{
  "intent": "book_appointment",
  "sentiment": "positive",
  "workflow_branch": "booking_requested",
  "recommended_next_action": "send_booking_link_or_create_sales_task",
  "confidence": 0.86
}
```

Suggested initial intents:

- `interested`,
- `not_interested`,
- `book_appointment`,
- `reschedule`,
- `pricing_question`,
- `support_request`,
- `payment_question`,
- `unsubscribe`,
- `wrong_number`,
- `needs_human`,
- `unknown`.

Implementation notes:

- Always make `unsubscribe` deterministic and high-priority.
- Keep output structured for workflow branching.
- Store no unnecessary message content beyond configured retention.

### 6. `check_message_risk`

Purpose:

Check whether message content is risky from a compliance, deliverability, or brand-safety perspective.

Input:

```json
{
  "channel": "SMS",
  "country": "US",
  "use_case": "marketing",
  "message": "Huge sale today. Click now!"
}
```

Output:

```json
{
  "risk": "medium",
  "issues": [
    "Marketing SMS should include opt-out language.",
    "Brand name is missing."
  ],
  "recommended_fix": "Add the brand name and STOP opt-out language.",
  "blocked": false
}
```

Implementation notes:

- Start with rules for known high-risk cases.
- Add LLM explanation after deterministic checks.
- Make the tool advisory by default, but allow enterprise policy to block high-risk sends.

### 7. `estimate_volume_and_cost`

Purpose:

Estimate message sends, channel mix, and cost before a workflow is activated.

Input:

```json
{
  "audience_size": 50000,
  "messages_per_recipient": 2,
  "fallback_rate": 0.15,
  "channels": ["WHATSAPP", "SMS"],
  "frequency": "monthly"
}
```

Output:

```json
{
  "estimated_messages": 115000,
  "channel_mix": {
    "WHATSAPP": 100000,
    "SMS": 15000
  },
  "estimated_customer_cost": 4200,
  "estimated_sinch_revenue": 4200,
  "currency": "USD",
  "assumptions": [
    "Primary message count equals audience size multiplied by messages per recipient.",
    "Fallback sends are estimated from fallback_rate."
  ]
}
```

Implementation notes:

- This does not need customer data lookup. The calling platform passes the audience size and workflow design.
- Use configured customer pricing where available; otherwise return volume only or a blended estimate.
- This tool is important for both customer approval and Sinch revenue attribution.

## Enterprise guardrails

AI agents can send real customer messages. The MCP product must be safe from the first release.

### Required controls

- OAuth or scoped API key authentication,
- tenant isolation,
- tool-level permissions,
- audit logs for every tool call,
- message preview in tool result where relevant,
- spend limits,
- rate limits,
- consent and opt-out enforcement,
- quiet-hour checks,
- approved-template-only mode,
- human approval requirement for bulk sends,
- webhook signing,
- allowlisted callback URLs,
- PII minimization,
- configurable retention.

### Suggested policy examples

```text
If use_case is marketing:
  require opt-in and opt-out language.

If audience_size is greater than 1000:
  require approval before send.

If estimated_customer_cost exceeds workspace limit:
  block send and return approval_required.

If channel is WhatsApp and message is business-initiated:
  require approved template.

If recipient has opted out:
  block send.
```

## MCP server implementation details

### Transport

Use a hosted remote MCP server.

Example endpoint:

```text
https://mcp.sinch.com/agent-actions
```

Rationale:

- enterprises need central auth,
- local-only MCP is not enough for production workflows,
- hosted MCP makes audit and policy enforcement possible,
- customers can connect any compatible client to the same endpoint.

### Authentication

Support two modes:

1. API key for developer preview and n8n templates.
2. OAuth 2.0 for enterprise and marketplace distribution.

Each request should resolve this context:

```json
{
  "sinch_account_id": "acc_123",
  "workspace_id": "workspace_456",
  "platform": "n8n",
  "external_user_id": "user_789",
  "allowed_tools": [
    "recommend_channel",
    "send_template_message",
    "get_delivery_status"
  ]
}
```

### Tool permissions

Example permission configuration:

```json
{
  "workspace_id": "workspace_456",
  "tools": {
    "recommend_channel": "allowed",
    "send_message": "approval_required",
    "send_template_message": "allowed",
    "get_delivery_status": "allowed",
    "classify_reply": "allowed",
    "check_message_risk": "allowed",
    "estimate_volume_and_cost": "allowed"
  },
  "limits": {
    "max_messages_per_day": 10000,
    "max_estimated_cost_per_workflow": 5000,
    "bulk_threshold": 1000
  }
}
```

### Audit event model

Every tool call should create an audit event.

```json
{
  "audit_id": "audit_456",
  "timestamp": "2026-05-31T09:00:00Z",
  "workspace_id": "workspace_456",
  "platform": "n8n",
  "tool": "send_template_message",
  "external_reference": "shopify_cart_123",
  "recipient_hash": "sha256:...",
  "channel": "WHATSAPP",
  "status": "queued",
  "policy_result": "allowed"
}
```

Avoid storing raw PII unless needed for support and configured by customer policy.

## Approach 1: n8n integration

### Why start here?

n8n is the fastest validation target for MCP-first execution:

- it has strong workflow automation usage,
- it supports AI agents and MCP client patterns,
- templates are easy to demonstrate,
- it can validate customer appetite before deeper CRM marketplace work.

### Integration model

```text
n8n trigger
        |
        v
n8n AI Agent node
        |
        | MCP client
        v
Sinch Agent Actions MCP Server
        |
        v
Sinch Conversation API or Sinch Engage
```

### What Sinch ships

- hosted MCP endpoint,
- authentication guide,
- n8n credential setup guide,
- reusable workflow templates,
- sample prompts,
- demo video,
- troubleshooting guide.

### Initial templates

#### Template 1: Abandoned cart recovery

```text
Shopify abandoned cart trigger
  -> AI agent calls recommend_channel
  -> AI agent calls send_template_message
  -> wait 10 minutes
  -> call get_delivery_status
  -> if failed, send SMS fallback
  -> update Shopify or CRM
```

Revenue logic:

```text
monthly abandoned carts
  x messages per cart
  x fallback rate
  x channel price
```

#### Template 2: Appointment reminder

```text
Calendar or CRM appointment trigger
  -> estimate_volume_and_cost
  -> send reminder
  -> classify reply
  -> branch to confirmed, reschedule, or needs_human
```

#### Template 3: Payment failure recovery

```text
Payment failed trigger
  -> check_message_risk
  -> recommend_channel
  -> send approved template
  -> classify reply
  -> update billing workflow
```

### Implementation steps

1. Create hosted MCP server with API-key auth.
2. Publish n8n setup doc with MCP server URL and credential steps.
3. Build three workflow templates.
4. Add tool-call examples and expected JSON outputs.
5. Pilot with internal solution engineers or existing automation-heavy customers.
6. Track messages sent with `platform = n8n`.

## Approach 2: enterprise custom agents

### Why it matters

Many enterprise customers are building their own agents with OpenAI, Anthropic, Azure AI, LangChain, LlamaIndex, CrewAI, internal platforms, or cloud AI services. These customers need a trusted communication tool.

### Integration model

```text
Enterprise AI agent
        |
        | MCP client
        v
Sinch Agent Actions MCP Server
        |
        v
Sinch communication APIs
```

### What Sinch ships

- remote MCP endpoint,
- MCP tool reference,
- example client configuration,
- sample prompts,
- security documentation,
- policy configuration guide,
- sandbox account.

### Example agent instruction

```text
When you need to contact a customer, use Sinch tools.
First call check_message_risk for generated text.
Then call recommend_channel.
Use send_template_message for business-initiated WhatsApp messages.
After sending, call get_delivery_status and summarize the result.
Never send marketing content unless consent is present in the supplied context.
```

### Example use case

```text
Payment system emits failed payment event
  -> enterprise agent receives event context
  -> agent calls recommend_channel
  -> agent calls send_template_message
  -> agent checks delivery
  -> agent writes result to customer system
```

### Implementation steps

1. Provide developer preview access to the MCP server.
2. Add example configurations for popular MCP clients.
3. Provide a sandbox template set for appointment, payment, delivery, and lead follow-up.
4. Add enterprise policy configuration.
5. Create reference architecture for regulated customers.

## Approach 3: HubSpot and Sinch Engage

### Important constraint

The current Sinch Engage HubSpot integration already supports SMS, MMS, RCS, WhatsApp, workflow automation, contact record messaging, templates, opt-out reporting, HubSpot Conversations Inbox, and HubSpot AI/Breeze usage.

Do not duplicate the existing integration.

### MCP-first opportunity

If HubSpot or a HubSpot-connected AI workflow can act as an MCP client, it should call the Sinch MCP server directly.

```text
HubSpot-connected AI agent
        |
        | MCP client
        v
Sinch Agent Actions MCP Server
        |
        v
Sinch Engage or Conversation API
```

### What to add with AI

Since Sinch does not need to look up HubSpot data for first release, use action-only tools. HubSpot or the external agent passes the needed context.

Best tools for HubSpot use cases:

- `recommend_channel`,
- `classify_reply`,
- `check_message_risk`,
- `estimate_volume_and_cost`,
- `send_template_message`.

### Example HubSpot flow

```text
HubSpot workflow identifies renewal-risk customer
  -> HubSpot-connected agent calls recommend_channel with contact context
  -> agent calls send_template_message
  -> inbound reply is passed to classify_reply
  -> HubSpot branches to sales task, renewal workflow, or support ticket
```

### What Sinch ships first

- MCP server documentation for HubSpot-connected agents,
- field mapping guide:
  - phone,
  - country,
  - opt-in status,
  - lifecycle stage,
  - deal stage,
  - message text,
  - use case,
- workflow examples that complement the existing HubSpot app,
- revenue estimator examples for HubSpot workflows.

### If native MCP is not available

Keep MCP as the core product, but optionally provide a thin adapter later:

```text
HubSpot workflow action
        |
        | HTTPS/OpenAPI adapter
        v
Sinch Agent Actions Gateway
        |
        v
same business logic as MCP tools
```

This adapter should not become a separate product. It is only a compatibility layer for platforms that do not yet act as MCP clients.

## Approach 4: Salesforce Agentforce

### MCP-first opportunity

If Agentforce or a Salesforce-connected enterprise agent can call external MCP tools, connect it directly to the Sinch MCP server.

```text
Agentforce or Salesforce-connected agent
        |
        | MCP client
        v
Sinch Agent Actions MCP Server
        |
        v
Sinch messaging APIs
```

### High-value use cases

- high-priority case update,
- payment reminder,
- appointment reminder,
- renewal follow-up,
- field service arrival notification,
- lead follow-up,
- outage or delivery update.

### Example Salesforce flow

```text
Case priority changes to High
  -> agent receives case and contact context
  -> agent calls check_message_risk
  -> agent calls recommend_channel
  -> agent calls send_template_message
  -> agent calls get_delivery_status
  -> Salesforce case is updated by the Salesforce-side workflow
```

### What Sinch ships first

- MCP server endpoint,
- Salesforce-oriented tool usage guide,
- approved template examples for service and sales,
- implementation guide for Salesforce architects,
- audit and compliance guide.

### If native MCP is not available

Use a thin OpenAPI adapter for Salesforce External Services or Agentforce Actions while keeping the backend shared with MCP:

```text
Salesforce Agentforce Action
        |
        | OpenAPI action
        v
Sinch Agent Actions Gateway
        |
        v
same tool logic used by MCP
```

This protects the MCP-first strategy while enabling enterprise pilots where Salesforce has not enabled direct MCP use.

## Approach 5: platform marketplaces and ecosystem

### Where marketplaces fit

Marketplaces help discovery and trust, but they should come after real workflow validation.

Suggested order:

1. hosted MCP server developer preview,
2. n8n templates and docs,
3. enterprise custom agent pilots,
4. HubSpot/Salesforce compatibility guides,
5. marketplace listings or app adapters after repeatable usage is proven.

### Marketplace assets

- "Connect Sinch MCP to your AI agent" landing page,
- "n8n AI workflows with Sinch" templates,
- "Salesforce agent communication actions" reference guide,
- "HubSpot AI workflow actions with Sinch Engage" reference guide,
- security and compliance one-pager,
- demo videos,
- ROI calculator based on message volume.

## Revenue attribution model

Every message created through the MCP server should be tagged.

Example tag:

```json
{
  "source": "sinch_agent_actions_mcp",
  "platform": "n8n",
  "workflow_id": "payment_failure_recovery",
  "tool": "send_template_message",
  "ai_agent_triggered": true
}
```

### Incremental volume formula

```text
Incremental messages =
audience size
x messages per recipient
x workflow activation rate
+ fallback messages
+ reply messages
```

### Revenue formula

```text
Revenue =
SMS sends x SMS rate
+ WhatsApp sends x WhatsApp rate
+ RCS sends x RCS rate
+ MMS sends x MMS rate
+ other channel sends x channel rate
+ optional platform or AI fee
```

### Example

```text
Workflow: payment failure recovery
Audience: 50,000 customers per month
Messages per recipient: 2
Fallback rate: 15%

Primary messages: 100,000
Fallback SMS messages: 15,000
Total messages: 115,000 per month
```

The product dashboard should show:

- estimated messages before activation,
- actual messages after activation,
- channel mix,
- fallback volume,
- delivery rate,
- reply rate,
- estimated Sinch revenue,
- customer outcome.

## Release plan

### Release 0: internal prototype

Scope:

- mock MCP server,
- three tools:
  - `recommend_channel`,
  - `estimate_volume_and_cost`,
  - `check_message_risk`,
- local demo with sample n8n or custom agent.

Goal:

Validate whether agents can reliably call Sinch tools and produce usable workflow decisions.

### Release 1: developer preview

Scope:

- hosted MCP server,
- API-key auth,
- seven core tools,
- Conversation API send path,
- delivery status ingestion,
- basic audit logs,
- n8n templates,
- sandbox templates.

Goal:

Prove real external workflows can create message volume.

### Release 2: enterprise pilot

Scope:

- OAuth,
- workspace policies,
- spend limits,
- approval requirements,
- approved-template-only mode,
- stronger audit exports,
- HubSpot and Salesforce implementation guides,
- selected customer pilots.

Goal:

Validate enterprise security, compliance, and revenue attribution.

### Release 3: ecosystem launch

Scope:

- public docs,
- ecosystem landing page,
- marketplace/listing work where appropriate,
- partner enablement,
- ROI calculator,
- reference architectures.

Goal:

Scale adoption through AI platforms, SIs, and existing Sinch customers.

## Build checklist

### Engineering

- [ ] hosted MCP server,
- [ ] Agent Actions Gateway,
- [ ] tool schema validation,
- [ ] API-key auth,
- [ ] OAuth plan,
- [ ] Conversation API integration,
- [ ] delivery webhook ingestion,
- [ ] audit logging,
- [ ] workspace policy engine,
- [ ] rate and spend limits,
- [ ] template send support,
- [ ] volume and cost estimator,
- [ ] reply classifier,
- [ ] message risk checker.

### Developer experience

- [ ] tool reference docs,
- [ ] n8n setup guide,
- [ ] custom agent setup guide,
- [ ] sample prompts,
- [ ] sample workflows,
- [ ] troubleshooting guide,
- [ ] sandbox credentials flow.

### Go to market

- [ ] landing page,
- [ ] demo video,
- [ ] n8n templates,
- [ ] HubSpot guide,
- [ ] Salesforce guide,
- [ ] partner/SI enablement,
- [ ] customer pilot list,
- [ ] ROI calculator.

## Recommended next step

Start with the MCP-first release:

1. Build the hosted MCP server and Agent Actions Gateway.
2. Ship the seven core tools.
3. Validate with n8n templates and one custom enterprise agent.
4. Use `estimate_volume_and_cost` and message tagging to prove incremental send volume.
5. Add HubSpot and Salesforce compatibility guides, then adapters only where native MCP is not available.

This keeps the product focused: third-party AI platforms integrate with Sinch through MCP, and Sinch earns revenue when those agents create safe, measurable messaging volume.
