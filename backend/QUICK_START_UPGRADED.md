# Quick Start Guide - Upgraded Backend

## Installation

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env and add your n8n webhook URLs
```

### 3. Start Backend Server
```bash
python main.py
```

Server will start on `http://localhost:8000`

## Testing the New Features

### Test Complete Analysis with All New Agents

```bash
# 1. Create a user
curl -X POST http://localhost:8000/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123"
  }'

# 2. Login
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'

# 3. Run Enhanced Analysis
curl -X POST http://localhost:8000/run-analysis \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "drug_name": "Aspirin",
    "indication": "Migraine"
  }' | jq .
```

### Expected Response Sections

The response will include all original sections PLUS:

1. **IQVIA_Market_Intelligence**
   - Market size and CAGR
   - Competitor analysis
   - Regional breakdown
   - Growth forecasts

2. **EXIM_Trade_Intelligence**
   - Export/import volumes
   - Trade balance
   - Top trading partners
   - Growth trends

3. **Mechanism_of_Action**
   - Primary molecular targets
   - Affected pathways
   - MoA relevance score
   - Binding affinity data

4. **PPI_Network**
   - Direct protein interactions
   - Indirect network pathways
   - Network topology metrics
   - PPI relevance score

5. **Disease_Similarity**
   - Approved indications
   - Multi-dimensional similarity metrics
   - Repurposing rationale
   - Similarity score

6. **Hypothesis_Generation**
   - 2-3 testable hypotheses
   - Supporting evidence
   - Testable predictions
   - Uncertainty flags

### Check n8n Webhook Logs

After running analysis, check your n8n instance for webhook calls:
- Analysis completion webhook
- Report generation webhook (after PDF creation)

## n8n Webhook Setup

### 1. IQVIA Mock Endpoint

Create an n8n workflow with a webhook trigger that returns:

```json
{
  "section": "IQVIA Market Intelligence",
  "market_size_usd_millions": 1500,
  "cagr_percent": 8.5,
  "current_market_share_percent": 15.2,
  "top_competitors": [
    {"name": "Competitor A", "market_share": 25.3},
    {"name": "Competitor B", "market_share": 18.7}
  ],
  "regional_breakdown": {
    "North America": 45,
    "Europe": 30,
    "Asia Pacific": 20,
    "Rest of World": 5
  },
  "forecast_2025": 1725,
  "forecast_2030": 2175,
  "key_insights": [
    "Strong market growth expected",
    "Increasing demand in emerging markets"
  ]
}
```

### 2. EXIM Mock Endpoint

Create an n8n workflow with a webhook trigger that returns:

```json
{
  "section": "EXIM Trade Intelligence",
  "total_exports_usd_millions": 250,
  "total_imports_usd_millions": 180,
  "trade_balance_usd_millions": 70,
  "top_export_destinations": [
    {"country": "United States", "value_usd_millions": 87.5},
    {"country": "Germany", "value_usd_millions": 62.5}
  ],
  "top_import_sources": [
    {"country": "China", "value_usd_millions": 72},
    {"country": "India", "value_usd_millions": 54}
  ],
  "trade_trends": {
    "export_growth_yoy_percent": 12.5,
    "import_growth_yoy_percent": 8.2,
    "trade_balance_trend": "Positive"
  }
}
```

### 3. Analysis Completion Webhook

Create an n8n workflow to receive analysis completion notifications:

**Webhook receives:**
```json
{
  "drug": "Aspirin",
  "indication": "Migraine",
  "feasibility_score": 78,
  "avg_confidence": 0.82,
  "timestamp": "2024-01-15T10:30:00",
  "status": "completed"
}
```

**Possible actions:**
- Send email notification
- Update database
- Trigger downstream workflows
- Log to monitoring system

### 4. Report Generation Webhook

Create an n8n workflow to receive PDF generation notifications:

**Webhook receives:**
```json
{
  "pdf_path": "reports/report_abc123.pdf",
  "report_id": "abc123",
  "drug": "Aspirin",
  "indication": "Migraine",
  "user_email": "user@example.com",
  "timestamp": "2024-01-15T10:35:00",
  "status": "completed"
}
```

**Possible actions:**
- Email PDF to user
- Upload to cloud storage
- Archive report
- Update CRM system

## Fallback Behavior

If n8n webhooks are not configured or fail:
- System automatically generates synthetic fallback data
- Analysis continues without interruption
- Quality notes indicate data source (real vs. synthetic)
- No errors thrown to user

## Monitoring

### Check Agent Execution

Watch console output for agent execution logs:
```
[Master Agent] Fetching IQVIA and EXIM data via n8n...
[MoA Agent] Analyzing mechanism for Aspirin...
[PPI Agent] Analyzing protein interaction networks...
[Disease Similarity Agent] Analyzing disease similarity for Aspirin → Migraine...
[Hypothesis Agent] Generating research hypotheses for Aspirin → Migraine...
[Master Agent] Sending analysis completion webhook to n8n...
[SUCCESS] n8n webhook sent to https://...
```

### Verify Scores

Check the enhanced highlights in response:
```json
{
  "highlights": {
    "feasibility_score": 78,
    "moa_score": 82,
    "ppi_score": 75,
    "similarity_score": 80,
    "avg_confidence": 0.82
  }
}
```

## Troubleshooting

### n8n Webhooks Not Working

**Symptom:** Fallback data always used

**Solutions:**
1. Check n8n webhook URLs in `.env`
2. Verify n8n workflows are active
3. Test webhooks manually with curl
4. Check n8n logs for errors
5. Verify network connectivity

### Import Errors

**Symptom:** `ModuleNotFoundError`

**Solutions:**
```bash
pip install requests pandas numpy
```

### Agent Execution Slow

**Symptom:** Analysis takes >30 seconds

**Solutions:**
- Check API rate limits
- Verify network connectivity
- Consider caching frequently accessed data
- Optimize n8n webhook response times

## Production Deployment

### Environment Variables

Set these in production:
```bash
SECRET_KEY=<strong-random-key>
N8N_WEBHOOK_REPORT_URL=https://prod-n8n.com/webhook/report
N8N_WEBHOOK_ANALYSIS_URL=https://prod-n8n.com/webhook/analysis
N8N_IQVIA_URL=https://prod-n8n.com/webhook/iqvia
N8N_EXIM_URL=https://prod-n8n.com/webhook/exim
```

### Security Considerations

1. Use HTTPS for all n8n webhooks
2. Implement webhook authentication
3. Rate limit webhook endpoints
4. Monitor webhook failures
5. Set up alerting for errors

## Next Steps

1. ✅ Backend upgraded with 5 new agents
2. ✅ n8n integration layer complete
3. ✅ Enhanced scoring algorithm implemented
4. ✅ Comprehensive documentation created
5. 🔄 Configure n8n workflows
6. 🔄 Test end-to-end workflow
7. 🔄 Deploy to production

## Support

For issues or questions:
1. Check `BACKEND_UPGRADE_COMPLETE.md` for detailed documentation
2. Review agent code in `backend/agents/`
3. Check console logs for error messages
4. Verify n8n webhook configurations
