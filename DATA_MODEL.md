# Data Model Documentation

Fill in these sections based on your specific needs.

---

## Race Events

What types of races do you need to support?
- [x] Road running (5K, 10K, half marathon, marathon)
- [x] Trail running (5K, 10K, half marathon, marathon, ultra)
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
| elevation_gain | float | No | Elevation gain in meters |
| surface | enum | No | road, trail, track, gravel |

### Data Sources

Which websites/APIs will you scrape?
- [x] Official race timing websites (utmb.world)
- [x] Race result aggregators (my.raceresult.com, runagain.com)
- [x] Official race websites for specific events (e.g. www.swissalps100.com/results.asp)
- [ ] Strava segments
- [ ] Other: _______________

---

## Athletes

### Athlete Entity Fields

| Field | Type | Required? | Description |
|-------|------|-----------|-------------|
| athlete_id | string | Yes | Unique identifier |
| name | string | Yes | Full name (may be anonymous) |
| age | int | No | Age at time of race |
| gender | enum | No | M, F, X |
| hometown | string | No | Location |

### How do you identify athletes?
- [x] By name
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
| gender | string | No | Gender (M/F/X)
| age_group_lower | int | No | Age group, lower bound |
| age_group_upper | int | No | Age group, upper bound |
| division_position | int | No | Position within division |
| finish_time | duration | Yes | Total time (HH:MM:SS) |
| pace | float | No | Average pace (min/km) |
| DNF/DNS | boolean | No | Did not finish/start |

### Missing Data Handling

What do you do when:
- Division info is missing: Leave blank, only use this result for calculations where division is not used
- Duplicate results: Deduplicate, store only one of the results

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
| Top 40% | Absolute best case |
| Top 45% | Strong performance, top half finish |
| Top 50% | Above average |
| Top 55% | Solid performance |

### Reference Data Needed

- Age grading tables for running?
- Equivalent performance calculators (Riegel, Cameron)?

---

## Data Storage

### Storage Approach

- [ ] SQLite (local, simple)
- [ ] PostgreSQL (production)
- [x] CSV/JSON files (flat files)
- [ ] In-memory only (no persistence)
- [ ] Other: _______________

### Data Retention

- Keep all historical data? Yes
- Archive old races after X years? Do not implement archiving (yet)
- Purge duplicates how? De-duplicate and merge results

---

## API/Integration Needs

| Integration | Purpose | Priority |
|-------------|---------|----------|
| Race timing APIs | Fetch results | High |
| Strava | Search race results and training history | Low |
| Weather data | Correlate performance | Low |
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