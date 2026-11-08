# Demo audio

The homepage sample players use these files. They are **synthesized placeholders** (neural text-to-speech, Hindi/Hinglish) so the player, waveform, and layout can ship before real call recordings are available. The page labels every clip “Demo audio”.

Drop a real recording on the same filename to replace a placeholder. Keep the name, or update the matching `src` in `index.html`.

| File | What it should be |
| --- | --- |
| `clinic-booking-hinglish.mp3` | Clinic appointment booking, ideally Hinglish |
| `missed-call-recovery.mp3` | Outbound missed-call recovery |
| `follow-up-reminder.mp3` | Appointment follow-up reminder |

MP3, mono, 64–128 kbps is enough. The player uses `preload="none"` and only draws the live Web Audio waveform after playback starts.

Recordings already in the repo, under different scenarios, and not wired to these three slots:

- `mp3/HealthCare-onboarding_cEIUBM4Y (1).mp3`
- `mp3/BFSI-reminder_dztcIGvN.mp3`
- `mp3/hospitality-front-desk_CVZtKlFn.mp3`
- `mp3/Ecom-customer-support_IRqJbynE.mp3`
- `mp3/Edtech-lead-qualification_KTkZSGKj.mp3`
- `mp3/recruitment_eczAKBnf.mp3`
