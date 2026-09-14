# Operation id <-> SDK function name — sinch-sdk-python

Snapshot of Confluence **"APIs Operation Ids <-> SDK functions mapping"** (space PF, page 812783650).
Page lastModified: **28 Aug 2026**.  Source: https://sinchenterprise.atlassian.net/wiki/spaces/PF/pages/812783650

Scoped to the domains this SDK implements. A domain absent from this file
is absent from **this SDK**, not necessarily from the page.

# Numbers API

| Tag | Operation id | SDK function |
|---|---|---|
| Available Number | `NumberService_RentAnyNumber` | `numbers.rentAny` |
| Available Number | `NumberService_RentNumber` | `numbers.rent` |
| Available Number | `NumberService_ListAvailableNumbers` | `numbers.searchForAvailableNumbers` |
| Available Number | `NumberService_GetAvailableNumber` | `numbers.checkAvailability` |
| Active Number | `NumberService_ListActiveNumbers` | `numbers.list` |
| Active Number | `NumberService_UpdateActiveNumber` | `numbers.update` |
| Active Number | `NumberService_GetActiveNumber` | `numbers.get` |
| Active Number | `NumberService_ReleaseNumber` | `numbers.release` |
| Active Number | `NumberService_GetEmergencyAddress` | `numbers.getEmergencyAddress` |
| Active Number | `NumberService_ProvisionEmergencyAddress` | `numbers.provisionEmergencyAddress` |
| Active Number | `NumberService_DeprovisionEmergencyAddress` | `numbers.deprovisionEmergencyAddress` |
| Active Number | `NumberService_ValidateEmergencyAddress` | `numbers.validateEmergencyAddress` |
| Available Regions | `NumberService_ListAvailableRegions` | `numbers.regions.list` |
| Callback Configuration | `GetCallbackConfiguration` | V1 numbers.callback.get / V2 numbers.callback_configuration.get |
| Callback Configuration | `UpdateCallbackConfiguration` | V1 numbers.callback.update / V2 numbers.eventDestinations.update |
| Webhooks | `(no operationId)` | V1 numbers.webhooks.parseEvent, numbers.webhooks.validateAuthenticationHeader / V2 numbers.sinchEvents.* |

# SMS API

| Tag | Operation id | SDK function |
|---|---|---|
| Batches | `SendSMS` | `sms.batches.send` (v2.0 proposal: sms.sendSMSBatch / sendMMSBatch / sendBinaryBatch) |
| Batches | `ListBatches` | `sms.batches.list` |
| Batches | `Dry_Run` | `sms.batches.dryRun` (+ dryRunSMS / dryRunMMS / dryRunBinary) |
| Batches | `GetBatchMessage` | `sms.batches.get` |
| Batches | `UpdateBatchMessage` | `sms.batches.update` (+ updateSMS / updateMMS / updateBinary) |
| Batches | `ReplaceBatch` | `sms.batches.replace` (+ replaceSMS / replaceMMS / replaceBinary) |
| Batches | `CancelBatchMessage` | `sms.batches.cancel` |
| Batches | `deliveryFeedback` | `sms.batches.sendDeliveryFeedback` |
| Inbounds | `ListInboundMessages` | `sms.inbounds.list` |
| Inbounds | `RetrieveInboundMessage` | `sms.inbounds.get` |
| Groups | `ListGroups` | `sms.groups.list` |
| Groups | `CreateGroup` | `sms.groups.create` |
| Groups | `RetrieveGroup` | `sms.groups.get` |
| Groups | `UpdateGroup` | `sms.groups.update` |
| Groups | `ReplaceGroup` | `sms.groups.replace` |
| Groups | `deleteGroup` | `sms.groups.delete` |
| Groups | `GetMembers` | `sms.groups.listMembers` |
| Delivery reports | `GetDeliveryReportByBatchId` | `sms.deliveryReports.get` |
| Delivery reports | `GetDeliveryReportByPhoneNumber` | `sms.deliveryReports.getForNumber` |
| Delivery reports | `getDeliveryReports` | `sms.deliveryReports.list` |
| Pricing | `getPricing` | `sms.pricing.get` |
| Webhooks | `(no operationId)` | V1 sms.webhooks.* / V2 sms.sinchEvents.validateAuthenticationHeader, parseEvent |

# Voice API

| Tag | Operation id | SDK function |
|---|---|---|
| Callouts | `Callouts` | `voice.callouts.textToSpeech / voice.callouts.conference / voice.callouts.custom` (one endpoint, three helpers) |
| Calls | `Calls` | voice.calls.get / voice.calls.update / voice.calls.manageWithCallLeg |
| Conferences | `Calling_GetConferenceInfo` | `voice.conferences.get` |
| Conferences | `Calling_KickConferenceAll` | `voice.conferences.kickAll` |
| Conferences | `Calling_ManageConferenceParticipant` | `voice.conferences.manageParticipant` |
| Conferences | `Calling_KickConferenceParticipant` | `voice.conferences.kickParticipant` |
| Conferences | `(duplicate of Calls tag)` | `voice.conferences.call` (identical to voice.callouts.conference) |
| Applications | `Configuration_GetNumbers` | `voice.applications.listNumbers` |
| Applications | `Configuration_UpdateNumbers` | `voice.applications.assignNumbers` |
| Applications | `Configuration_UnassignNumber` | `voice.applications.unassignNumber` |
| Applications | `Configuration_GetCallbackURLs` | `voice.applications.getCallbackUrls` |
| Applications | `Configuration_UpdateCallbackURLs` | `voice.applications.updateCallbackUrls` |
| Applications | `Calling_QueryNumber` | `voice.applications.queryNumber` |
| Webhooks | `(no operationId)` | V1 voice.webhooks.* / V2 voice.sinchEvents.validateAuthenticationHeader, parseEvent, serializeResponse |

# Voice API v2

The second Voice table on the Confluence page. Separate operations from the
Voice v1 table above.
| Operation id | Path | SDK function |
|---|---|---|
| `createCall` | `POST /v2/projects/{projectId}/calls` | `voice.v2.calls.create` (see open question) |
| `getBatchCallSummary` | `GET /v2/projects/{projectId}/batches/{batchId}` | `voice.v2.batches.get` |
| `stopBatchProcessing` | `DELETE /v2/projects/{projectId}/batches/{batchId}` | `voice.v2.batches.stop` |
| `getBatchDetails` | `GET /v2/projects/{projectId}/batches/{batchId}/details` | `voice.v2.batches.getDetails` |
| `getSessionById` | `GET /v2/projects/{projectId}/sessions/{sessionId}` | `voice.v2.sessions.get` |

`projectId` is a structural path parameter — never a public method parameter.
It comes from the client configuration.

### Two errors on the page — the spec wins

1. The **details** row on Confluence repeats the operation id `getBatchCallSummary`.
   The spec calls it **`getBatchDetails`** (`voice-v2.yaml:1047`). The SDK name is unaffected.
2. The **Sessions** row writes the path as `/sessions/{batchId}`. The spec has
   **`/sessions/{sessionId}`** (`voice-v2.yaml:891`).

### One open question — do not resolve alone

`createCall` is undecided on the page: `voice.v2.calls.create` **or**
`voice.v2.calls.start`, plus a proposed batch helper `voice.v2.batches.create`
wrapping the same endpoint. Use `create`; if asked to rename or add the helper,
STOP and ask.

### Not on Confluence — derived, NOT authoritative

Present in the spec, absent from the page. Adding any of these to the public
surface requires extending the page first — see the DECISION RULE.

`listCalls`, `getCallById`, `patchCallById`, `patchCallBySessionAndName`,
`listServices`, `createService`, `getService`, `updateService`, `deleteService`,
`describeSvaml`, `validateSvaml`.

`callWebhook` is a server-side callback and a duplicate of `validateSvaml` —
not exposed by client SDKs.

# Conversation API

| Tag | Operation id | SDK function |
|---|---|---|
| Messages | `Messages_SendMessage` | `conversation.messages.sendMessage (+ sendCardMessage, sendCarouselMessage, sendChoiceMessage, sendContactInfoMessage, sendLocationMessage, sendListMessage, sendMediaMessage, sendTemplateMessage, sendTextMessage)` |
| Messages | `Messages_GetMessage` | `conversation.messages.get` |
| Messages | `Messages_DeleteMessage` | `conversation.messages.delete` |
| Messages | `Messages_ListMessages` | `conversation.messages.list` |
| Messages | `Messages_UpdateMessageMetadata` | `conversation.messages.update` |
| Messages | `Messages_ListMessagesByChannelIdentity` | `conversation.messages.listLastMessagesByChannelIdentity` |
| Apps | `App_ListApps` | `conversation.apps.list` |
| Apps | `App_CreateApp` | `conversation.apps.create` |
| Apps | `App_GetApp` | `conversation.apps.get` |
| Apps | `App_DeleteApp` | `conversation.apps.delete` |
| Apps | `App_UpdateApp` | `conversation.apps.update` |
| Contacts | `Contact_ListContacts` | `conversation.contacts.list` |
| Contacts | `Contact_CreateContact` | `conversation.contacts.create` |
| Contacts | `Contact_GetContact` | `conversation.contacts.get` [page reads 'conversation.contact.sget' - typo] |
| Contacts | `Contact_DeleteContact` | `conversation.contacts.delete` |
| Contacts | `Contact_UpdateContact` | `conversation.contacts.update` |
| Contacts | `Contact_MergeContact` | `conversation.contacts.mergeContact` |
| Contacts | `Contact_GetChannelProfile` | `conversation.contacts.getChannelProfile (+ ByContactId, ByChannelIdentity)` |
| Contacts | `Contact_ListIdentityConflicts` | `conversation.contacts.listIdentityConflicts` |
| Consents | `Consents_GetConsents` | `conversation.consents.listIdentities` |
| Consents | `Consents_GetConsentsAuditRecords` | `conversation.consents.listAuditRecords` |
| Conversations | `Conversation_ListConversations` | `conversation.conversations.list` |
| Conversations | `Conversation_ListRecentConversations` | `conversation.conversations.listRecent` |
| Conversations | `Conversation_CreateConversation` | `conversation.conversations.create` |
| Conversations | `Conversation_GetConversation` | `conversation.conversations.get` |
| Conversations | `Conversation_DeleteConversation` | `conversation.conversations.delete` |
| Conversations | `Conversation_UpdateConversation` | `conversation.conversations.update` |
| Conversations | `Conversation_StopActiveConversation` | `conversation.conversations.stopActive` |
| Conversations | `Conversation_InjectMessage` | `conversation.conversations.injectMessage` |
| Conversations | `Events_InjectEvent` | `conversation.conversations.injectEvent` |
| Events | `Events_SendEvent` | `conversation.events.send` |
| Events | `Events_GetEvent` | `conversation.events.get` |
| Events | `Events_ListEvents` | `conversation.events.list` |
| Events | `Events_DeleteEvents` | `conversation.events.delete` |
| Project Settings | `ProjectSettings_GetSettings` | `conversation.projectsettings.get` |
| Project Settings | `ProjectSettings_CreateSettings` | `conversation.projectsettings.create` |
| Project Settings | `ProjectSettings_UpdateSettings` | `conversation.projectsettings.update` |
| Project Settings | `ProjectSettings_DeleteSettings` | `conversation.projectsettings.delete` |
| Transcoding | `Transcoding_TranscodeMessage` | `conversation.transcoding.transcodeMessage` |
| Capability | `Capability_QueryCapability` | `conversation.capability.lookup` |
| Callback configuration | `Webhooks_ListWebhooks` | V1 conversation.webhooks.list / V2 conversation.eventDestinations.list |
| Callback configuration | `Webhooks_CreateWebhook` | V1 conversation.webhooks.create / V2 conversation.eventDestinations.create |
| Callback configuration | `Webhooks_GetWebhook` | V1 conversation.webhooks.get / V2 conversation.eventDestinations.get |
| Callback configuration | `Webhooks_UpdateWebhook` | V1 conversation.webhooks.update / V2 conversation.eventDestinations.update |
| Callback configuration | `Webhooks_DeleteWebhook` | V1 conversation.webhooks.delete / V2 conversation.eventDestinations.delete |
| TemplatesV2 | `Templates_v2_ListTemplates` | `conversation.templatesV2.list` |
| TemplatesV2 | `Templates_v2_CreateTemplate` | `conversation.templatesV2.create` |
| TemplatesV2 | `Templates_v2_ListTranslations` | `conversation.templatesV2.listTranslations` |
| TemplatesV2 | `Templates_v2_UpdateTemplate` | `conversation.templatesV2.update` |
| TemplatesV2 | `Templates_v2_GetTemplate` | `conversation.templatesV2.get` |
| TemplatesV2 | `Templates_v2_DeleteTemplate` | `conversation.templatesV2.delete` |
| TemplatesV1 | `Templates_* (DEPRECATED at API level 31 Jan 2026)` | `conversation.templatesV1.*` - do not add new work here |
| Webhooks | `(no operationId)` | V1 conversation.webhooks.* / V2 conversation.sinchEvents.validateAuthenticationHeader, parseEvent |

# Number Lookup API

| Tag | Operation id | SDK function |
|---|---|---|
| Number Lookup | `NumberLookupV2_Lookup` | `number_lookup.lookup` |
