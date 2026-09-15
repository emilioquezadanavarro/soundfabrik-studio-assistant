# Eval results

_Generated 2026-09-15 20:24 UTC_

## Retrieval (21/21 cases passed)

**recall@5**: 1.00 · **MRR**: 0.84

| Case | Result | Detail |
|---|---|---|
| What rooms does Klangraum Berlin have? | PASS | expected one of ('home.md',), got ['studio-a.md', 'home.md', 'faq.md', 'services.md', 'studio-b.md'] |
| Who has recorded at the studio? | PASS | expected one of ('home.md',), got ['home.md', 'services.md', 'home.md', 'faq.md', 'home.md'] |
| Which room should I choose for a full band? | PASS | expected one of ('faq.md', 'studio-a.md'), got ['faq.md', 'faq.md', 'studio-b.md', 'services.md', 'home.md'] |
| Can I record drums in Studio South? | PASS | expected one of ('faq.md', 'studio-b.md'), got ['faq.md', 'faq.md', 'faq.md', 'home.md', 'services.md'] |
| Can I bring my own laptop and DAW? | PASS | expected one of ('faq.md', 'studio-b.md'), got ['faq.md', 'studio-b.md', 'studio-b.md', 'studio-a.md', 'faq.md'] |
| Do I need to book an engineer or can I work alone? | PASS | expected one of ('faq.md',), got ['faq.md', 'faq.md', 'faq.md', 'faq.md', 'faq.md'] |
| How much does a session cost? | PASS | expected one of ('faq.md',), got ['faq.md', 'faq.md', 'faq.md', 'faq.md', 'studio-b.md'] |
| How do I book a session? | PASS | expected one of ('faq.md',), got ['faq.md', 'faq.md', 'faq.md', 'faq.md', 'services.md'] |
| Do you offer mixing without recording? | PASS | expected one of ('faq.md',), got ['faq.md', 'services.md', 'services.md', 'faq.md', 'faq.md'] |
| Do you do immersive audio? | PASS | expected one of ('faq.md', 'studio-b.md', 'services.md'), got ['faq.md', 'studio-b.md', 'services.md', 'faq.md', 'studio-b.md'] |
| What services do you offer besides recording? | PASS | expected one of ('services.md',), got ['services.md', 'faq.md', 'services.md', 'home.md', 'faq.md'] |
| Can I rehearse for a tour at the studio? | PASS | expected one of ('services.md', 'faq.md'), got ['services.md', 'faq.md', 'faq.md', 'faq.md', 'faq.md'] |
| Can I shoot a music video there? | PASS | expected one of ('services.md',), got ['faq.md', 'services.md', 'faq.md', 'home.md', 'faq.md'] |
| What's in Studio North's live room? | PASS | expected one of ('studio-a.md',), got ['home.md', 'studio-b.md', 'studio-a.md', 'faq.md', 'services.md'] |
| What piano do you have? | PASS | expected one of ('studio-a.md',), got ['studio-a.md', 'studio-a.md', 'studio-a.md', 'studio-b.md', 'home.md', 'studio-b.md', 'faq.md'] |
| What monitoring does Studio South have? | PASS | expected one of ('studio-b.md',), got ['home.md', 'studio-b.md', 'faq.md', 'faq.md', 'services.md'] |
| What plugins are available in Studio South? | PASS | expected one of ('studio-b.md',), got ['studio-b.md', 'home.md', 'studio-a.md', 'studio-a.md', 'studio-b.md'] |
| Who is on the team? | PASS | expected one of ('team.md',), got ['team.md', 'studio-a.md', 'faq.md', 'studio-a.md', 'studio-b.md', 'team.md', 'team.md', 'faq.md'] |
| Who is the owner of the studio? | PASS | expected one of ('team.md',), got ['home.md', 'studio-b.md', 'team.md', 'studio-b.md', 'studio-a.md', 'team.md', 'faq.md', 'faq.md', 'team.md'] |
| What's your address? | PASS | expected one of ('contact.md',), got ['faq.md', 'contact.md', 'home.md', 'faq.md', 'services.md'] |
| How do I contact the studio? | PASS | expected one of ('contact.md', 'faq.md'), got ['faq.md', 'team.md', 'faq.md', 'faq.md', 'home.md'] |

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

## Answer quality (10/12 cases passed)

**pass_rate**: 0.83 · **grounded_rate**: 0.83 · **scope_rate**: 1.00

| Case | Result | Detail |
|---|---|---|
| What's the difference between Studio North and Studio South? | PASS | grounded=True scope=True reply="We call them Studio A and Studio B, not North and South, but I'm happy to explain the difference.\n\nStudio A is our large" |
| Can I record a full band in Studio South? | FAIL | grounded=False scope=True reply="Not on its own. Studio B (South) is a control and listening room with no live room of its own, so it's not set up for tr" |
| Can I bring my own DAW? | FAIL | grounded=False scope=True reply='Yes, absolutely. Studio B is set up for plug-and-play, so you can integrate your own notebook and DAW with our gear via ' |
| How much does a session cost? | PASS | grounded=True scope=True reply='Rates are quoted per project rather than a fixed price, since they depend on which studio you need, how many days or hou' |
| Who do I contact to book a session? | PASS | grounded=True scope=True reply='Robin Regner, our studio manager, is your main contact for bookings. Send him your project details and preferred dates a' |
| Do you offer mixing without recording? | PASS | grounded=True scope=True reply='Yes, absolutely. You can bring finished recordings to us for mixing, and you have two options: have one of our experienc' |
| Do you do immersive audio? | PASS | grounded=True scope=True reply="Yes, we do! \nStudio B has a 7.1.4 immersive setup built with Eve Audio, and we offer mixing in Dolby Atmos.\n It's a form" |
| Can I use the studio for tour rehearsals? | PASS | grounded=True scope=True reply='Yes, absolutely. We offer Studio A, our 90-square-meter live room, as a rehearsal space for bands preparing for a tour o' |
| Who is the owner of the studio? | PASS | grounded=True scope=True reply='Soundfabrik Berlin has two owners: \nGuilherme Castelhano, who handles business relations\n, and \nJulia Selbherr Castelhan' |
| Do you have a drum kit I can use? | PASS | grounded=True scope=True reply='Yes, we do. Studio A has two drum kits available: a Premier late 1960s 202 and a Ludwig Classic Maple. We also have a co' |
| What's the best pizza place near the studio? | PASS | grounded=True scope=True reply='I can only help with questions about Soundfabrik Berlin itself, the studios, gear, services, and booking. For restaurant' |
| What's your address? | PASS | grounded=True scope=True reply="We're at Salzufer 15-16, 10587 Berlin, on the top floor of a historic factory building. If you need help with parking, v" |
