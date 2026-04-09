# Data Model Documentation

Fill in these sections based on your specific needs.

---

## Race Events

What types of races do you need to support?
- [ ] Running (5K, 10K, half marathon, marathon, ultra)
- [ ] Cycling (road, mountain bike, gravel)
- [ ] Swimming
- [ ] Triathlon
- [ ] Other: _______________

### Race Entity Fields

| Field | Type | Required? | Description |
|-------|------|-----------|-------------|
| event_id | string | Yes | Unique identifier |
| name | string | Yes | Event name |
| date | date | Yes | Event date |
| location | string | No | City, region, country |
| discipline | enum | Yes | running, cycling, swimming, triathlon |
| distance | float | Yes | Distance in meters |
| distance_unit | enum | Yes | km, miles |
| surface | enum | No | road, trail, track, gravel |

### Data Sources

Which websites/APIs will you scrape?
- [ ] Official race timing websites (list which)
- [ ] Race result aggregators (e.g., Athlinks, Sportstats)
- [ ] Strava segments
- [ ] Other: _______________

---

## Athletes

### Athlete Entity Fields

| Field | Type | Required? | Description |
|-------|------|-----------|-------------|
| athlete_id | string | Yes | Unique identifier |
| name | string | No | Full name (may be anonymous) |
| age | int | No | Age at time of race |
| gender | enum | No | male, female, non-binary |
| hometown | string | No | Location |

### How do you identify athletes?
- [ ] By name (prone to duplicates)
- [ ] By timing platform ID
- [ ] By Strava/connected account
- [ ] Other: _______________

---

## Race Results

### Result Entity Fields

| Field | Type | Required? | Description |
|-------|------|-----------|-------------|
| result_id | string | Yes | Unique identifier |
| race_id | string | Yes | Foreign key to race |
| athlete_id | string | Yes | Foreign key to athlete |
| position | int | Yes | Overall finish position |
| division | string | No | Age group, gender division |
| division_position | int | No | Position within division |
| finish_time | duration | Yes | Total time (HH:MM:SS) |
| split_times | array | No | Intermediate splits |
| pace | float | No | Average pace (min/km or min/mi) |
| DNF/DNS | boolean | No | Did not finish/start |

### Missing Data Handling

What do you do when:
- Splits are missing: _______________
- Division info is missing: _______________
- Duplicate results: _______________

---

## Performance Calculations

### Metrics to Calculate

| Metric | Description | Formula/Method |
|--------|-------------|----------------|
| percentile_rank | What percentile is this result? | position / total_finishers * 100 |
| age_grade | Performance adjusted for age | TBD - requires age grading tables |
| equivalent_time | Equivalent time for different distance | TBD - use Riegel formula? |
| projected_time | Predicted time based on training | TBD |

### Percentile Targets

| Target | Example Use Case |
|--------|------------------|
| Top 1% | Elite qualifier |
| Top 10% | Age group podium |
| Top 25% | Top quarter finish |
| Top 50% | Above average |

### Reference Data Needed

- Age grading tables for running/cycling?
- Equivalent performance calculators (Riegel, Cameron)?
- Course-specific adjustments?

---

## Data Storage

### Storage Approach

- [ ] SQLite (local, simple)
- [ ] PostgreSQL (production)
- [ ] CSV/JSON files (flat files)
- [ ] In-memory only (no persistence)
- [ ] Other: _______________

### Data Retention

- Keep all historical data? Yes / No
- Archive old races after X years? _______________
- Purge duplicates how? _______________

---

## API/Integration Needs

| Integration | Purpose | Priority |
|-------------|---------|----------|
| Strava | Import activities | High / Medium / Low |
| Race timing APIs | Fetch results | High / Medium / Low |
| Weather data | Correlate performance | High / Medium / Low |
| Other | | |

---

## Next Steps

1. Choose 1-2 race result sources to start with
2. Define the minimum viable data schema
3. Build scraper for one source
4. Implement basic percentile calculation
5. Create first CLI command

---

_This document should be updated as the project evolves._