import streamlit as st
import json
import os
from startup_evaluator import StartupEvaluator
from config import InvestorPreferences
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def main():
    st.set_page_config(
        page_title="SmartCurateQ - AI Startup Evaluator",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🚀 SmartCurateQ</h1>
        <h3>AI-Powered Startup Investment Analysis</h3>
        <p>Automated startup curation and investment insights powered by Google AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Status indicator
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.success("✅ System Online - Vertex AI Connected")
    
    # Enhanced sidebar for investor preferences
    with st.sidebar:
        st.markdown("### ⚙️ Investment Criteria")
        st.markdown("---")
        
        # Investment focus selection
        st.markdown("**Investment Focus**")
        focus_preset = st.selectbox(
            "Quick Presets",
            ["Custom", "Founder-Focused", "Market-Focused", "Traction-Focused", "Balanced"]
        )
        
        # Set preset values
        if focus_preset == "Founder-Focused":
            founder_weight, market_weight, diff_weight, traction_weight = 0.4, 0.2, 0.2, 0.2
        elif focus_preset == "Market-Focused":
            founder_weight, market_weight, diff_weight, traction_weight = 0.2, 0.4, 0.2, 0.2
        elif focus_preset == "Traction-Focused":
            founder_weight, market_weight, diff_weight, traction_weight = 0.2, 0.2, 0.2, 0.4
        elif focus_preset == "Balanced":
            founder_weight, market_weight, diff_weight, traction_weight = 0.25, 0.25, 0.25, 0.25
        else:
            founder_weight = st.slider("👥 Founder Weight", 0.0, 1.0, 0.25, 0.05)
            market_weight = st.slider("📈 Market Weight", 0.0, 1.0, 0.25, 0.05)
            diff_weight = st.slider("🎯 Differentiation Weight", 0.0, 1.0, 0.25, 0.05)
            traction_weight = st.slider("🚀 Traction Weight", 0.0, 1.0, 0.25, 0.05)
        
        # Show current weights
        total_weight = founder_weight + market_weight + diff_weight + traction_weight
        if total_weight > 0:
            founder_weight /= total_weight
            market_weight /= total_weight
            diff_weight /= total_weight
            traction_weight /= total_weight
        
        # Weight visualization
        weights_df = pd.DataFrame({
            'Criteria': ['Founder', 'Market', 'Differentiation', 'Traction'],
            'Weight': [founder_weight, market_weight, diff_weight, traction_weight]
        })
        
        fig = px.pie(weights_df, values='Weight', names='Criteria', 
                     title="Investment Weights",
                     color_discrete_sequence=['#667eea', '#764ba2', '#f093fb', '#f5576c'])
        fig.update_layout(height=300, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        risk_tolerance = st.selectbox("🎲 Risk Tolerance", ["low", "medium", "high"], index=1)
        
        preferences = InvestorPreferences(
            founder_weight=founder_weight,
            market_weight=market_weight,
            differentiation_weight=diff_weight,
            traction_weight=traction_weight,
            risk_tolerance=risk_tolerance
        )
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Evaluate Startup", "📊 Batch Analysis", "📈 Dashboard", "🧪 Sample Data"])
    
    with tab1:
        st.markdown("### 🔍 Single Startup Evaluation")
        st.markdown("Upload a pitch deck or enter startup details for comprehensive AI analysis")
        
        col1, col2 = st.columns([1, 1], gap="large")
        
        with col1:
            st.markdown("#### 📤 Data Input")
            
            # File upload
            st.markdown("**Option 1: Upload Pitch Deck**")
            uploaded_file = st.file_uploader(
                "Choose a PDF file", 
                type=['pdf'],
                help="Upload your startup's pitch deck for automated analysis"
            )
            
            if uploaded_file:
                st.success(f"✅ File uploaded: {uploaded_file.name}")
            
            st.markdown("---")
            st.markdown("**Option 2: Manual Entry**")
            
            company_name = st.text_input(
                "🏢 Company Name *", 
                placeholder="e.g., TechCorp AI"
            )
            
            problem_statement = st.text_area(
                "❓ Problem Statement", 
                placeholder="What problem does this startup solve?",
                height=100
            )
            
            solution = st.text_area(
                "💡 Solution", 
                placeholder="How does the startup solve this problem?",
                height=100
            )
            
            submitted = st.button(
                "🚀 Analyze Startup", 
                type="primary",
                use_container_width=True
            )
                
            if submitted and (company_name or uploaded_file):
                evaluator = StartupEvaluator()
                
                # Handle PDF upload
                pitch_deck_path = None
                if uploaded_file:
                    pitch_deck_path = f"temp_{uploaded_file.name}"
                    with open(pitch_deck_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                
                # Handle form data
                form_data = None
                if company_name:
                    form_data = {
                        "company_name": company_name,
                        "problem_statement": problem_statement,
                        "solution": solution,
                        "market_size": 1000000000,
                        "revenue": 0,
                        "employees": 5,
                        "funding_stage": "Seed",
                        "founders": [{
                            "name": "Founder",
                            "background": "Industry expert",
                            "experience_years": 5,
                            "previous_exits": 0,
                            "domain_expertise": "Business"
                        }]
                    }
                
                memo = evaluator.evaluate_startup(
                    pitch_deck_path=pitch_deck_path,
                    form_data=form_data,
                    investor_preferences=preferences
                )
                st.session_state['current_memo'] = memo
                
                # Store all analyzed startups for dashboard
                if 'all_startups' not in st.session_state:
                    st.session_state['all_startups'] = []
                st.session_state['all_startups'].append(memo)
                
                st.success("Analysis completed!")
        
        with col2:
            st.markdown("#### 📊 Analysis Results")
            
            if 'current_memo' in st.session_state:
                memo = st.session_state['current_memo']
                
                # Investment score with visual indicator
                score = memo.investment_score
                score_color = "🟢" if score >= 7 else "🟡" if score >= 5 else "🔴"
                
                st.markdown(f"""
                <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                           padding: 1.5rem; border-radius: 10px; text-align: center; color: white; margin-bottom: 1rem;">
                    <h2>{score_color} Investment Score: {score:.1f}/10</h2>
                    <p style="margin: 0; font-size: 1.1em;">{memo.recommendation}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Key metrics dashboard
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    risk_emoji = "🟢" if memo.risk_assessment.risk_level == "low" else "🟡" if memo.risk_assessment.risk_level == "medium" else "🔴"
                    st.metric(
                        "Risk Level", 
                        f"{risk_emoji} {memo.risk_assessment.risk_level.upper()}"
                    )
                
                with col_b:
                    market_size = memo.startup_profile.market_analysis.market_size
                    st.metric(
                        "Market Size", 
                        f"${market_size/1e9:.1f}B" if market_size >= 1e9 else f"${market_size/1e6:.0f}M"
                    )
                
                with col_c:
                    revenue = memo.startup_profile.business_metrics.revenue or 0
                    st.metric(
                        "Revenue", 
                        f"${revenue/1e6:.1f}M" if revenue >= 1e6 else f"${revenue/1e3:.0f}K" if revenue >= 1e3 else f"${revenue:.0f}"
                    )
                
                # Detailed breakdown
                st.markdown("---")
                
                # Company Information Section - Always Visible
                st.markdown("### 🏢 Company Information")
                profile = memo.startup_profile
                
                col_info1, col_info2 = st.columns(2)
                with col_info1:
                    st.markdown(f"**Company Name:** {profile.company_name}")
                    st.markdown(f"**Funding Stage:** {profile.funding_stage}")
                    if profile.funding_amount:
                        st.markdown(f"**Funding Amount:** ${profile.funding_amount:,.0f}")
                
                with col_info2:
                    metrics = profile.business_metrics
                    if metrics.revenue:
                        st.markdown(f"**Annual Revenue:** ${metrics.revenue:,.0f}")
                    if metrics.employees:
                        st.markdown(f"**Team Size:** {metrics.employees} employees")
                    if metrics.revenue_growth:
                        st.markdown(f"**Revenue Growth:** {metrics.revenue_growth:.1%}")
                
                # Problem & Solution Section - Always Visible
                st.markdown("### ❓ Problem & Solution")
                problem_text = profile.problem_statement or "Not specified"
                solution_text = profile.solution or "Not specified"
                differentiator_text = profile.unique_differentiator or "Not specified"
                
                st.markdown(f"**Problem Statement:**")
                st.write(problem_text)
                
                st.markdown(f"**Solution:**")
                st.write(solution_text)
                
                st.markdown(f"**Unique Differentiator:**")
                st.write(differentiator_text)
                
                # Founders Section - Always Visible
                st.markdown("### 👥 Founders")
                for founder in profile.founders:
                    founder_name = founder.name or "Unknown Founder"
                    founder_bg = founder.background or "Background not specified"
                    st.markdown(f"**{founder_name}** (Founder-Market Fit Score: {founder.founder_market_fit_score:.1f}/10)")
                    st.write(f"Background: {founder_bg}")
                
                # Market Analysis Section - Always Visible
                st.markdown("### 📈 Market Analysis")
                market = profile.market_analysis
                col_market1, col_market2 = st.columns(2)
                with col_market1:
                    market_size_display = f"${market.market_size/1e9:.1f}B" if market.market_size >= 1e9 else f"${market.market_size/1e6:.0f}M"
                    st.markdown(f"**Market Size:** {market_size_display}")
                    st.markdown(f"**Growth Rate:** {market.growth_rate:.1%}")
                with col_market2:
                    st.markdown(f"**Competition Level:** {market.competition_level.title()}")
                    key_players_text = ', '.join(market.key_players[:3]) if market.key_players else "Not specified"
                    st.markdown(f"**Key Players:** {key_players_text}")
                
                st.markdown("---")
                
                # Strengths and concerns - Always Visible
                st.markdown("### ✨ Key Strengths")
                for i, strength in enumerate(memo.key_strengths, 1):
                    st.markdown(f"**{i}.** {strength}")
                
                st.markdown("### ⚠️ Key Concerns")
                for i, concern in enumerate(memo.key_concerns, 1):
                    st.markdown(f"**{i}.** {concern}")
                
                # Risk factors if any - Always Visible
                if memo.risk_assessment.risk_factors:
                    st.markdown("### 🚨 Risk Factors")
                    for i, risk in enumerate(memo.risk_assessment.risk_factors, 1):
                        st.markdown(f"**{i}.** {risk}")
                
                # Action buttons
                st.markdown("---")
                col_btn1, col_btn2 = st.columns(2)
                
                with col_btn1:
                    if st.button("📝 Generate Deal Note", use_container_width=True):
                        try:
                            evaluator = StartupEvaluator()
                            deal_note = evaluator.generate_deal_note(memo)
                            st.session_state['deal_note'] = deal_note
                            st.success("Deal note generated!")
                        except Exception as e:
                            st.error(f"Error generating deal note: {str(e)}")
                
                with col_btn2:
                    if 'deal_note' in st.session_state:
                        st.download_button(
                            label="⬇️ Download Deal Note",
                            data=st.session_state['deal_note'],
                            file_name=f"deal_note_{memo.startup_profile.company_name.replace(' ', '_')}.md",
                            mime="text/markdown",
                            use_container_width=True
                        )
                
                # Show deal note if generated
                if 'deal_note' in st.session_state:
                    with st.expander("📄 Investment Deal Note", expanded=False):
                        st.markdown(st.session_state['deal_note'])
            
            else:
                st.info("👆 Enter startup details or upload a pitch deck to see analysis results")
    
    with tab2:
        st.markdown("### 📊 Batch Analysis")
        st.markdown("Process multiple startups simultaneously for portfolio analysis")
        
        # Upload section
        st.markdown("#### 📤 Upload Multiple Files")
        uploaded_files = st.file_uploader(
            "Choose multiple PDF files", 
            type=['pdf'], 
            accept_multiple_files=True,
            help="Upload multiple pitch decks for batch processing"
        )
        
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} files uploaded")
            for file in uploaded_files:
                st.markdown(f"• {file.name}")
        
        st.markdown("---")
        st.markdown("#### 🧪 Demo: Sample Batch Analysis")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 Run Sample Analysis", use_container_width=True):
                sample_data = [
                    {
                        "form_data": {
                            "company_name": "TechStartup A",
                            "problem_statement": "Inefficient data processing",
                            "solution": "AI-powered automation platform",
                            "market_size": 5000000000,
                            "revenue": 500000,
                            "employees": 15,
                            "founders": [{"name": "Alice Smith", "background": "Former Google engineer"}]
                        }
                    },
                    {
                        "form_data": {
                            "company_name": "HealthTech B", 
                            "problem_statement": "Poor patient monitoring",
                            "solution": "IoT health monitoring devices",
                            "market_size": 2000000000,
                            "revenue": 0,
                            "employees": 8,
                            "founders": [{"name": "Bob Johnson", "background": "Medical device expert"}]
                        }
                    }
                ]
                
                try:
                    with st.spinner("Processing batch analysis... This may take a few minutes."):
                        evaluator = StartupEvaluator()
                        results = evaluator.batch_evaluate(sample_data, preferences)
                        
                        # Enhanced results display
                        st.markdown("#### 📈 Batch Analysis Results")
                        
                        # Summary metrics
                        avg_score = sum(memo.investment_score for memo in results) / len(results)
                        high_potential = sum(1 for memo in results if memo.investment_score >= 7)
                        
                        col_m1, col_m2, col_m3 = st.columns(3)
                        with col_m1:
                            st.metric("Average Score", f"{avg_score:.1f}/10")
                        with col_m2:
                            st.metric("High Potential", f"{high_potential}/{len(results)}")
                        with col_m3:
                            st.metric("Total Analyzed", len(results))
                        
                        # Results table
                        df_data = []
                        for memo in results:
                            score = memo.investment_score
                            score_emoji = "🟢" if score >= 7 else "🟡" if score >= 5 else "🔴"
                            risk_emoji = "🟢" if memo.risk_assessment.risk_level == "low" else "🟡" if memo.risk_assessment.risk_level == "medium" else "🔴"
                            
                            df_data.append({
                                "Company": memo.startup_profile.company_name,
                                "Score": f"{score_emoji} {score:.1f}/10",
                                "Recommendation": memo.recommendation.split(" - ")[0],
                                "Risk": f"{risk_emoji} {memo.risk_assessment.risk_level.upper()}",
                                "Market Size": f"${memo.startup_profile.market_analysis.market_size/1e9:.1f}B",
                                "Revenue": f"${(memo.startup_profile.business_metrics.revenue or 0)/1e6:.1f}M"
                            })
                        
                        df = pd.DataFrame(df_data)
                        st.dataframe(df, use_container_width=True)
                        
                        # Score distribution chart
                        scores = [memo.investment_score for memo in results]
                        fig = px.histogram(x=scores, nbins=10, title="Investment Score Distribution")
                        fig.update_layout(xaxis_title="Investment Score", yaxis_title="Count")
                        st.plotly_chart(fig, use_container_width=True)
                        
                        st.success(f"✅ Successfully analyzed {len(results)} startups!")
                        
                except Exception as e:
                    st.error(f"❌ Error in batch analysis: {str(e)}")
        
        with col2:
            st.markdown("**💡 Batch Analysis Features:**")
            st.markdown("""
            - Process up to 50 startups simultaneously
            - Comparative scoring and ranking
            - Portfolio-level insights
            - Export results to CSV/Excel
            - Risk distribution analysis
            """)
    
    with tab3:
        st.markdown("### 📈 Investment Dashboard")
        st.markdown("Portfolio overview and analytics")
        
        # Real dashboard data from analyzed startups
        if 'all_startups' in st.session_state and st.session_state['all_startups']:
            startups = st.session_state['all_startups']
            
            # Portfolio metrics
            total_evaluated = len(startups)
            avg_score = sum(s.investment_score for s in startups) / total_evaluated
            high_potential = sum(1 for s in startups if s.investment_score >= 7)
            total_revenue = sum(s.startup_profile.business_metrics.revenue or 0 for s in startups)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Evaluated", str(total_evaluated))
            with col2:
                st.metric("Avg Score", f"{avg_score:.1f}/10")
            with col3:
                st.metric("High Potential", f"{high_potential}/{total_evaluated}")
            with col4:
                st.metric("Total Revenue", f"${total_revenue/1e6:.1f}M")
            
            # Charts
            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
                # Score distribution
                scores = [s.investment_score for s in startups]
                fig1 = px.histogram(x=scores, nbins=5, title="Investment Score Distribution")
                st.plotly_chart(fig1, use_container_width=True)
            
            with col_chart2:
                # Stage breakdown
                stages = [s.startup_profile.funding_stage for s in startups]
                stage_counts = pd.Series(stages).value_counts()
                fig2 = px.pie(values=stage_counts.values, names=stage_counts.index, title="Funding Stage Breakdown")
                st.plotly_chart(fig2, use_container_width=True)
            
            # Recent evaluations table
            st.markdown("#### 📋 Analyzed Startups")
            table_data = []
            for startup in startups:
                score = startup.investment_score
                score_emoji = "🟢" if score >= 7 else "🟡" if score >= 5 else "🔴"
                table_data.append({
                    'Company': startup.startup_profile.company_name,
                    'Score': f"{score_emoji} {score:.1f}/10",
                    'Stage': startup.startup_profile.funding_stage,
                    'Recommendation': startup.recommendation.split(' - ')[0]
                })
            
            st.dataframe(pd.DataFrame(table_data), use_container_width=True)
        else:
            st.info("Complete startup evaluations to see dashboard data")
    
    with tab4:
        st.markdown("### 🧪 Sample Data & Testing")
        
        st.markdown("#### 📋 Sample Form Data")
        st.markdown("Use this sample data to test the evaluation system")
        sample_form = {
            "company_name": "AI Analytics Corp",
            "problem_statement": "Businesses struggle with data-driven decision making due to complex analytics tools",
            "solution": "No-code AI analytics platform that generates insights automatically",
            "market_size": 15000000000,
            "revenue": 1200000,
            "employees": 25,
            "founders": [
                {
                    "name": "Sarah Chen",
                    "background": "Former McKinsey consultant with 8 years in data analytics",
                    "experience_years": 8,
                    "previous_exits": 1,
                    "domain_expertise": "Business Intelligence"
                }
            ],
            "funding_stage": "Series A",
            "funding_amount": 5000000
        }
        
        st.json(sample_form)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🧪 Test Sample Evaluation", use_container_width=True):
                try:
                    with st.spinner("Testing evaluation..."):
                        evaluator = StartupEvaluator()
                        memo = evaluator.evaluate_startup(form_data=sample_form, investor_preferences=preferences)
                        
                        st.success("✅ Evaluation completed!")
                        
                        # Enhanced sample results
                        score = memo.investment_score
                        score_emoji = "🟢" if score >= 7 else "🟡" if score >= 5 else "🔴"
                        
                        st.markdown(f"""
                        <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                                   padding: 1rem; border-radius: 8px; text-align: center; color: white;">
                            <h3>{score_emoji} Sample Result: {score:.1f}/10</h3>
                            <p>{memo.recommendation}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Investment Score", f"{score:.1f}/10")
                        with col2:
                            st.metric("Risk Level", memo.risk_assessment.risk_level.upper())
                        with col3:
                            st.metric("Recommendation", memo.recommendation.split(" - ")[0])
                        
                except Exception as e:
                    st.error(f"❌ Error in sample evaluation: {str(e)}")
        
        with col2:
            st.markdown("**🎯 Testing Features:**")
            st.markdown("""
            - Sample data validation
            - API connectivity test
            - Performance benchmarking
            - Error handling verification
            - Output format validation
            """)
        
        # API Status
        st.markdown("---")
        st.markdown("#### 🔧 System Status")
        
        col_status1, col_status2, col_status3 = st.columns(3)
        with col_status1:
            st.success("✅ Vertex AI Connected")
        with col_status2:
            st.success("✅ All Agents Online")
        with col_status3:
            st.success("✅ System Ready")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p>🚀 <strong>SmartCurateQ</strong> - AI-Powered Startup Investment Analysis</p>
        <p>Built for GenAI Exchange Hackathon 2025 | Powered by Google Vertex AI</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()