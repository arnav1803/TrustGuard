import logging
import asyncio
import json
import pandas as pd
from datetime import datetime
import os
import glob
import index.css
# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Import your pipeline
from verification import ClaimVerificationPipeline
from processing.claim_extraction import ClaimExtractor



async def run_complete_pipeline(input_csv_path: str, output_report_path: str = None):
    """Run the complete pipeline from CSV input to verification report"""

    print("🚀 Starting Enhanced Claim Verification Pipeline with Knowledge Graph")
    print("=" * 70)

    try:
        extractor = ClaimExtractor()

        # Step 1: Load and validate CSV
        print("📊 Step 1: Loading and validating CSV data...")

        if not pd.io.common.file_exists(input_csv_path):
            raise FileNotFoundError(f"CSV file not found: {input_csv_path}")

        df = pd.read_csv(input_csv_path)
        print(f"✅ Loaded CSV with {len(df)} rows and columns: {list(df.columns)}")

        # Identify relevant columns
        text_columns = ['cleaned_text', 'text', 'content', 'body', 'message', 'post_text']
        id_columns = ['id', 'post_id', 'ID', 'Id']

        text_col = next((col for col in text_columns if col in df.columns), None)
        id_col = next((col for col in id_columns if col in df.columns), 'index')

        if not text_col:
            text_col = next((col for col in df.columns if df[col].dtype == 'object'), None)

        if not text_col:
            raise ValueError("No suitable text column found in CSV")

        print(f"📝 Using text column: '{text_col}', ID column: '{id_col}'")

        # Step 2: Extract claims
        print("🔍 Step 2: Extracting claims from posts...")
        all_claims = []

        for index, row in df.iterrows():
            text = str(row.get(text_col, '')).strip()
            post_id = str(row.get(id_col, f'post_{index}'))

            if text and len(text) > 20:
                claims = extractor.extract_claims_from_text(text, post_id)
                all_claims.extend(claims)

        print(f"✅ Extracted {len(all_claims)} claims from {len(df)} posts")

        if not all_claims:
            print("⚠️ No claims extracted. Check your data format.")
            return {"error": "No claims extracted from the data"}

        # Step 3: Select high-priority claims
        high_priority_claims = [c for c in all_claims if c.confidence in ['high', 'medium']] or all_claims
        high_priority_claims = high_priority_claims[:10]  # Limit for demo

        print(f"🎯 Selected {len(high_priority_claims)} claims for verification")

        print("\n📋 Selected Claims:")
        for i, claim in enumerate(high_priority_claims, 1):
            print(f"  {i}. [{claim.confidence}] {claim.text[:80]}...")

        # Step 4: Verify claims
        print("\n🔍 Step 3: Running verification pipeline...")
        pipeline = ClaimVerificationPipeline()
        results = await pipeline.verify_batch_claims(high_priority_claims)
        print(f"✅ Verification completed for {len(results)} claims")

        # Step 5: Generate and save report
        print("📋 Step 4: Generating verification report...")
        report = pipeline.generate_report(results)

        if output_report_path:
            with open(output_report_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"💾 Report saved to: {output_report_path}")

        # Step 6: Summary
        print("\n📊 VERIFICATION SUMMARY")
        print("=" * 40)
        summary = report['summary']
        print(f"Total Claims Processed: {summary['total_claims_processed']}")
        print(f"Average Processing Time: {summary['average_processing_time']}s")
        print(f"Success Rate: {summary['success_rate']}%")
        print("\nVerification Status Distribution:")
        for status, count in summary['verification_status_distribution'].items():
            print(f"  {status.replace('_', ' ').title()}: {count}")
        print("\nConfidence Distribution:")
        for level, count in summary['confidence_distribution'].items():
            print(f"  {level.title()}: {count}")

        if report['detailed_results']:
            print("\n🔍 Example Verification Results:")
            for i, result in enumerate(report['detailed_results'][:3], 1):
                print(f"\n{i}. Claim ID: {result['claim_id']}")
                print(f"   Status: {result['verification_status'].replace('_', ' ').title()}")
                print(f"   Confidence: {result['confidence_score']}")
                print(f"   Evidence Sources: {result['evidence_count']}")
                print(f"   Reasoning: {result['reasoning']}")

        print("\n✅ Pipeline completed successfully!")
        return report

    except Exception as e:
        error_msg = f"Pipeline error: {str(e)}"
        print(f"❌ {error_msg}")
        logging.error(error_msg)
        return {"error": error_msg}
    
def main():
    import asyncio
    from verification import ClaimVerificationPipeline
    from processing.claim_extraction import ClaimExtractor
    import logging

    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Replace with your async pipeline call
    input_csv = "data/processed_data/preprocessed_reddit_posts_with_topics.csv"
    output_path = "src/output/report.json"

    # Ensure the pipeline runs inside event loop
    asyncio.run(run_complete_pipeline(input_csv_path=input_csv, output_report_path=output_path))


if __name__ == "__main__":
    main()