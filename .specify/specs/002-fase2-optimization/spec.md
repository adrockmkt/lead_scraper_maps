# Feature Specification: Fase 2 - Otimização de Custo e Performance

## Overview
Implement cost and performance optimizations for the Lead Scraper Maps project to enable controlled API usage, dry-run testing, and comprehensive execution metrics.

## Problem Statement
The current pipeline lacks fine-grained control over API consumption, making it difficult to:
- Test functionality without incurring API costs
- Control execution scope by niches or regions
- Monitor performance and cost metrics
- Implement production-safe testing workflows

## Proposed Solution
Implement a comprehensive optimization layer with:
1. **DRY_RUN Mode**: Simulation mode without API calls
2. **Dynamic Limits**: Per-niche and per-neighborhood execution limits
3. **CLI Controls**: Command-line interface for execution control
4. **Metrics System**: Performance tracking and cost estimation
5. **Cost Reporting**: API consumption and cost analysis

## Key Features

### 1. DRY_RUN Mode
- Simulates complete pipeline execution without API calls
- Uses cached data where available
- Generates mock responses for missing data
- Reports estimated API calls and costs

### 2. Dynamic Limits
- Configurable limits per niche (max results)
- Configurable limits per bairro/region
- Global execution limits
- Graceful handling of API rate limits

### 3. CLI Controls
- `--dry-run`: Enable simulation mode
- `--nichos`: Comma-separated list of nichos to process
- `--bairros`: Comma-separated list of bairros to process
- `--limite-global`: Maximum total results
- `--limite-por-nicho`: Maximum results per niche
- `--verbose`: Detailed output

### 4. Metrics System
- Execution time per niche and bairro
- API call count and type tracking
- Success/failure rates
- Performance bottlenecks identification

### 5. Cost Reporting
- Estimated API costs based on Google Places API pricing
- Cost per niche breakdown
- Monthly cost projections
- Usage recommendations

## Success Criteria
- [ ] DRY_RUN mode completes without any API calls
- [ ] Dynamic limits prevent over-execution
- [ ] CLI interface provides intuitive controls
- [ ] Metrics accurately track performance
- [ ] Cost reports provide actionable insights
- [ ] Zero breaking changes to existing functionality

## Dependencies
- Existing Google Places API integration
- Current SQLite cache system
- Existing CSV output structure

## Non-Goals
- Changes to core scraping logic
- New data sources or APIs
- Changes to lead scoring algorithm
- Database schema modifications

## Risks and Mitigations
- **Risk**: Increased complexity in CLI interface
  **Mitigation**: Comprehensive help text and defaults
- **Risk**: Performance overhead from metrics collection
  **Mitigation**: Optional metrics with minimal overhead
- **Risk**: Inaccurate cost estimation
  **Mitigation**: Regular pricing updates and validation

## Timeline Estimate
- Implementation: 2-3 days
- Testing: 1-2 days
- Documentation: 1 day
- Total: 4-6 days

## Deliverables
1. Enhanced main pipeline with CLI interface
2. Updated Places client with dry-run support
3. Metrics collection and reporting service
4. Comprehensive test suite
5. Documentation and usage examples