# Eval results

_Generated 2026-09-15 10:18 UTC_

## Retrieval (21/21 cases passed)

**recall@5**: 1.00 · **MRR**: 0.98

| Case | Result | Detail |
|---|---|---|
| What rooms does Klangraum Berlin have? | PASS | expected one of ('home.md',), got ['home.md', 'faq.md', 'contact.md', 'services.md', 'faq.md'] |
| Who has recorded at the studio? | PASS | expected one of ('home.md',), got ['home.md', 'home.md', 'faq.md', 'faq.md', 'services.md'] |
| Which room should I choose for a full band? | PASS | expected one of ('faq.md', 'studio-a.md'), got ['faq.md', 'studio-a.md', 'services.md', 'studio-b.md', 'home.md'] |
| Can I record drums in Studio South? | PASS | expected one of ('faq.md', 'studio-b.md'), got ['faq.md', 'faq.md', 'faq.md', 'studio-b.md', 'home.md'] |
| Can I bring my own laptop and DAW? | PASS | expected one of ('faq.md', 'studio-b.md'), got ['faq.md', 'studio-b.md', 'studio-a.md', 'studio-a.md', 'faq.md'] |
| Do I need to book an engineer or can I work alone? | PASS | expected one of ('faq.md',), got ['faq.md', 'faq.md', 'faq.md', 'home.md', 'team.md'] |
| How much does a session cost? | PASS | expected one of ('faq.md',), got ['faq.md', 'faq.md', 'faq.md', 'services.md', 'home.md'] |
| How do I book a session? | PASS | expected one of ('faq.md',), got ['faq.md', 'services.md', 'faq.md', 'faq.md', 'services.md'] |
| Do you offer mixing without recording? | PASS | expected one of ('faq.md',), got ['faq.md', 'services.md', 'studio-b.md', 'faq.md', 'home.md'] |
| Do you do immersive audio? | PASS | expected one of ('faq.md', 'studio-b.md', 'services.md'), got ['faq.md', 'studio-b.md', 'home.md', 'studio-b.md', 'services.md'] |
| What services do you offer besides recording? | PASS | expected one of ('services.md',), got ['services.md', 'faq.md', 'services.md', 'home.md', 'faq.md'] |
| Can I rehearse for a tour at the studio? | PASS | expected one of ('services.md', 'faq.md'), got ['services.md', 'faq.md', 'faq.md', 'faq.md', 'services.md'] |
| Can I shoot a music video there? | PASS | expected one of ('services.md',), got ['services.md', 'faq.md', 'faq.md', 'faq.md', 'faq.md'] |
| What's in Studio North's live room? | PASS | expected one of ('studio-a.md',), got ['studio-a.md', 'home.md', 'faq.md', 'services.md', 'studio-b.md'] |
| What piano do you have? | PASS | expected one of ('studio-a.md',), got ['studio-a.md', 'studio-a.md', 'studio-b.md', 'home.md', 'studio-b.md'] |
| What monitoring does Studio South have? | PASS | expected one of ('studio-b.md',), got ['home.md', 'studio-b.md', 'faq.md', 'studio-b.md', 'faq.md'] |
| What plugins are available in Studio South? | PASS | expected one of ('studio-b.md',), got ['studio-b.md', 'home.md', 'faq.md', 'faq.md', 'faq.md'] |
| Who is on the team? | PASS | expected one of ('team.md',), got ['team.md', 'team.md', 'studio-a.md', 'studio-b.md', 'home.md', 'home.md', 'services.md', 'faq.md'] |
| Who is the owner of the studio? | PASS | expected one of ('team.md',), got ['team.md', 'home.md', 'studio-a.md', 'faq.md', 'home.md', 'team.md'] |
| What's your address? | PASS | expected one of ('contact.md',), got ['contact.md', 'faq.md', 'faq.md', 'studio-b.md', 'services.md'] |
| How do I contact the studio? | PASS | expected one of ('contact.md', 'faq.md'), got ['faq.md', 'faq.md', 'contact.md', 'services.md', 'team.md'] |

## Guard (22/22 cases passed)

**precision**: 1.00 · **recall**: 1.00

| Case | Result | Detail |
|---|---|---|
| What's the difference between Studio North and Studio South? | PASS | expected ALLOW, got ALLOW |
| Do you have a Neumann U87 I could use? | PASS | expected ALLOW, got ALLOW |
| Do you offer mastering as a standalone service? | PASS | expected ALLOW, got ALLOW |
| Can I get Dolby Atmos mixing done there? | PASS | expected ALLOW, got ALLOW |
| How much would a two-day session cost? | PASS | expected ALLOW, got ALLOW |
| Are you available next Friday? | PASS | expected ALLOW, got ALLOW |
| I'd like a quote for mixing my EP. | PASS | expected ALLOW, got ALLOW |
| Who should I talk to about booking? | PASS | expected ALLOW, got ALLOW |
| Where exactly is the studio located? | PASS | expected ALLOW, got ALLOW |
| Is there parking nearby for loading in gear? | PASS | expected ALLOW, got ALLOW |
| Hi there! | PASS | expected ALLOW, got ALLOW |
| Thanks, that's really helpful. | PASS | expected ALLOW, got ALLOW |
| My name is Jana and I'm working on a jazz album. | PASS | expected ALLOW, got ALLOW |
| What's the best mic placement for a grand piano session? | PASS | expected ALLOW, got ALLOW |
| What's the best pizza place near Neukölln? | PASS | expected REFUSE, got REFUSE |
| Any good bars to check out in Berlin tonight? | PASS | expected REFUSE, got REFUSE |
| What hotels do you recommend nearby? | PASS | expected REFUSE, got REFUSE |
| What's the weather forecast for tomorrow? | PASS | expected REFUSE, got REFUSE |
| What do you think about the upcoming election? | PASS | expected REFUSE, got REFUSE |
| Who won the World Cup in 2018? | PASS | expected REFUSE, got REFUSE |
| Can you help me debug my Python script? | PASS | expected REFUSE, got REFUSE |
| What's a good recipe for banana bread? | PASS | expected REFUSE, got REFUSE |

## Answer quality (12/12 cases passed)

**pass_rate**: 1.00 · **grounded_rate**: 1.00 · **scope_rate**: 1.00

| Case | Result | Detail |
|---|---|---|
| What's the difference between Studio North and Studio South? | PASS | grounded=True scope=True reply='Studio North is our live room, built for recording full bands, ensembles, and rehearsals. It has a 70m² space with a Yam' |
| Can I record a full band in Studio South? | PASS | grounded=True scope=True reply='Not really, Studio South is a control and listening room without its own live room. Use Studio North for full-band track' |
| Can I bring my own DAW? | PASS | grounded=True scope=True reply="Yes, absolutely. \nStudio South is built around a plug-and-play workflow, and you're welcome to bring your own laptop and" |
| How much does a session cost? | PASS | grounded=True scope=True reply='Rates are quoted per project depending on the room, duration, and whether you want an engineer. To send you a custom quo' |
| Who do I contact to book a session? | PASS | grounded=True scope=True reply='Lena Aumann, our studio manager, handles scheduling and bookings. You can reach us at info@klangraum-berlin.example or +' |
| Do you offer mixing without recording? | PASS | grounded=True scope=True reply="Yes, we do. You can bring finished recordings for mixing, or book Studio South to mix your own production there, it's se" |
| Do you do immersive audio? | PASS | grounded=True scope=True reply='Yes, we do. Studio South has a 5.1.4 immersive setup and we offer mixing in immersive formats on request, perfect if you' |
| Can I use the studio for tour rehearsals? | PASS | grounded=True scope=True reply="Yes, Studio North's live room is available as a rehearsal space for touring bands. To get started, reach out to Lena Aum" |
| Who is the owner of the studio? | PASS | grounded=True scope=True reply='Klangraum Berlin has two owners: **Lena Aumann** and **Mateo Ferreira**. Lena is also the studio manager and handles sch' |
| Do you have a drum kit I can use? | PASS | grounded=True scope=True reply="The context I have doesn't list a drum kit in either room's equipment. That said, you're welcome to bring your own drum " |
| What's the best pizza place near the studio? | PASS | grounded=True scope=True reply='I can only help with questions about Klangraum Berlin itself, the studios, gear, services, and booking. For restaurant r' |
| What's your address? | PASS | grounded=True scope=True reply="We're at Weserstraße 12, 12047 Berlin. Happy to help you plan a visit or answer any questions about the studios." |
