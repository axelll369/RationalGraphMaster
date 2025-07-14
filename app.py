import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from sympy import symbols, apart, limit, oo, solve, factor, cancel
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json
import os
from game_logic import GameLogic
from function_generator import FunctionGenerator
from database import Database

# Initialize components
@st.cache_resource
def init_components():
    return GameLogic(), FunctionGenerator(), Database()

def main():
    st.set_page_config(
        page_title="Graph Quest: Rational Rampage",
        page_icon="🎮",
        layout="wide"
    )
    
    # Initialize session state
    if 'game_state' not in st.session_state:
        st.session_state.game_state = 'menu'
    if 'player_name' not in st.session_state:
        st.session_state.player_name = ""
    if 'current_score' not in st.session_state:
        st.session_state.current_score = 0
    if 'current_round' not in st.session_state:
        st.session_state.current_round = 1
    if 'total_rounds' not in st.session_state:
        st.session_state.total_rounds = 5
    if 'current_function' not in st.session_state:
        st.session_state.current_function = None
    if 'hints_used' not in st.session_state:
        st.session_state.hints_used = 0
    if 'round_completed' not in st.session_state:
        st.session_state.round_completed = False
    if 'last_feedback' not in st.session_state:
        st.session_state.last_feedback = None
    
    game_logic, func_gen, db = init_components()
    
    # Header
    st.title("🎮 Graph Quest: Rational Rampage")
    st.markdown("---")
    
    # Game state management
    if st.session_state.game_state == 'menu':
        show_main_menu(game_logic, func_gen, db)
    elif st.session_state.game_state == 'playing':
        show_game_interface(game_logic, func_gen, db)
    elif st.session_state.game_state == 'game_over':
        show_game_over(game_logic, func_gen, db)
    elif st.session_state.game_state == 'leaderboard':
        show_leaderboard(db)

def show_main_menu(game_logic, func_gen, db):
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🎯 Welcome to Rational Function Adventures!")
        st.markdown("""
        **Master the art of graphing rational functions!**
        
        In this game, you'll:
        - 📈 Identify vertical and horizontal asymptotes
        - 🕳️ Find holes in rational functions
        - 📍 Locate x and y intercepts
        - ∞ Analyze end behavior and limits
        """)
        
        st.markdown("### 🏆 Game Rules")
        st.markdown("""
        - **5 rounds** of increasing difficulty
        - **100 points** per correct answer
        - **-10 points** for hints used
        - **Speed bonus** for quick answers
        """)
        
        # Player name input
        player_name = st.text_input("Enter your name:", value=st.session_state.player_name)
        
        col_start, col_board = st.columns(2)
        
        with col_start:
            if st.button("🚀 Start Game", type="primary", use_container_width=True):
                if player_name.strip():
                    st.session_state.player_name = player_name.strip()
                    st.session_state.game_state = 'playing'
                    st.session_state.current_score = 0
                    st.session_state.current_round = 1
                    st.session_state.hints_used = 0
                    st.session_state.round_completed = False
                    st.session_state.last_feedback = None
                    st.session_state.current_function = None
                    st.rerun()
                else:
                    st.error("Please enter your name to start!")
        
        with col_board:
            if st.button("📊 Leaderboard", use_container_width=True):
                st.session_state.game_state = 'leaderboard'
                st.rerun()

def show_game_interface(game_logic, func_gen, db):
    # Game header
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.metric("👤 Player", st.session_state.player_name)
    with col2:
        st.metric("🎯 Round", f"{st.session_state.current_round}/{st.session_state.total_rounds}")
    with col3:
        st.metric("⭐ Score", st.session_state.current_score)
    
    st.markdown("---")
    
    # Check for next round button click
    if st.session_state.round_completed:
        col_next = st.columns([1, 2, 1])[1]
        with col_next:
            if st.session_state.current_round < st.session_state.total_rounds:
                if st.button("➡️ Next Round", type="primary", use_container_width=True, key="next_round_btn"):
                    st.session_state.current_round += 1
                    st.session_state.current_function = None
                    st.session_state.hints_used = 0
                    st.session_state.round_completed = False
                    st.session_state.last_feedback = None
                    st.rerun()
            else:
                if st.button("🏁 Finish Game", type="primary", use_container_width=True, key="finish_game_btn"):
                    # Save score to database
                    db.save_score(st.session_state.player_name, st.session_state.current_score)
                    st.session_state.game_state = 'game_over'
                    st.rerun()
        
        # Show last round's feedback if available
        if st.session_state.last_feedback:
            st.markdown("### 📝 Round Results")
            feedback_data = st.session_state.last_feedback
            
            if feedback_data['score'] > 80:
                st.success(f"🎉 Excellent! +{feedback_data['points_earned']} points")
            elif feedback_data['score'] > 60:
                st.info(f"👍 Good job! +{feedback_data['points_earned']} points")
            else:
                st.warning(f"📚 Keep studying! +{feedback_data['points_earned']} points")
            
            with st.expander("📝 Detailed Feedback", expanded=True):
                for key, value in feedback_data['feedback'].items():
                    if value['correct']:
                        st.success(f"✅ {key.replace('_', ' ').title()}: {value['message']}")
                    else:
                        st.error(f"❌ {key.replace('_', ' ').title()}: {value['message']}")
        return
    
    # Generate or get current function
    if st.session_state.current_function is None:
        difficulty = min(st.session_state.current_round, 3)  # Cap difficulty at 3
        st.session_state.current_function = func_gen.generate_function(difficulty)
    
    func_data = st.session_state.current_function
    
    # Display function
    st.markdown(f"### Round {st.session_state.current_round}: Analyze this rational function")
    st.latex(func_data['latex'])
    
    # Create two columns for graph and questions
    col_graph, col_questions = st.columns([1.2, 1])
    
    with col_graph:
        st.markdown("#### 📈 Function Graph")
        fig = create_function_plot(func_data)
        st.plotly_chart(fig, use_container_width=True)
    
    with col_questions:
        st.markdown("#### 🎯 Identify the Features")
        
        # Vertical Asymptotes
        st.markdown("**Vertical Asymptotes:**")
        va_input = st.text_input("Enter x-values separated by commas (e.g., 2, -3):", key=f"va_input_{st.session_state.current_round}")
        
        # Horizontal Asymptotes
        st.markdown("**Horizontal Asymptote:**")
        ha_input = st.text_input("Enter y-value or 'none' (e.g., 0, 2, none):", key=f"ha_input_{st.session_state.current_round}")
        
        # Holes
        st.markdown("**Holes:**")
        holes_input = st.text_input("Enter x-values separated by commas or 'none':", key=f"holes_input_{st.session_state.current_round}")
        
        # X-intercepts
        st.markdown("**X-intercepts:**")
        x_int_input = st.text_input("Enter x-values separated by commas or 'none':", key=f"x_int_input_{st.session_state.current_round}")
        
        # Y-intercept
        st.markdown("**Y-intercept:**")
        y_int_input = st.text_input("Enter y-value or 'undefined':", key=f"y_int_input_{st.session_state.current_round}")
        
        # Action buttons
        col_submit, col_hint = st.columns(2)
        
        with col_submit:
            if st.button("✅ Submit Answers", type="primary", use_container_width=True, key=f"submit_{st.session_state.current_round}"):
                answers = {
                    'vertical_asymptotes': va_input,
                    'horizontal_asymptote': ha_input,
                    'holes': holes_input,
                    'x_intercepts': x_int_input,
                    'y_intercept': y_int_input
                }
                
                score, feedback = game_logic.check_answers(func_data, answers)
                points_earned = max(0, score - (st.session_state.hints_used * 10))
                st.session_state.current_score += points_earned
                
                # Store feedback for next display
                st.session_state.last_feedback = {
                    'score': score,
                    'points_earned': points_earned,
                    'feedback': feedback
                }
                
                # Mark round as completed
                st.session_state.round_completed = True
                st.rerun()
        
        with col_hint:
            if st.button("💡 Get Hint", use_container_width=True, key=f"hint_{st.session_state.current_round}"):
                if st.session_state.hints_used < 3:
                    hint = game_logic.get_hint(func_data, st.session_state.hints_used)
                    st.session_state.hints_used += 1
                    st.info(f"💡 Hint: {hint}")
                else:
                    st.warning("No more hints available!")

def show_game_over(game_logic, func_gen, db):
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🎉 Game Complete!")
        st.markdown(f"**Final Score: {st.session_state.current_score} points**")
        
        # Show rank
        scores = db.get_leaderboard()
        rank = len([s for s in scores if s['score'] > st.session_state.current_score]) + 1
        st.markdown(f"**Your Rank: #{rank}**")
        
        # Achievement badges
        achievements = []
        if st.session_state.current_score >= 450:
            achievements.append("🏆 Rational Master")
        if st.session_state.current_score >= 350:
            achievements.append("🎯 Asymptote Ace")
        if st.session_state.hints_used == 0:
            achievements.append("🧠 No Hints Hero")
        if st.session_state.current_score >= 200:
            achievements.append("📈 Graph Guru")
        
        if achievements:
            st.markdown("### 🏅 Achievements Unlocked!")
            for achievement in achievements:
                st.markdown(f"- {achievement}")
        
        col_play, col_board, col_menu = st.columns(3)
        
        with col_play:
            if st.button("🔄 Play Again", type="primary", use_container_width=True):
                st.session_state.game_state = 'playing'
                st.session_state.current_score = 0
                st.session_state.current_round = 1
                st.session_state.current_function = None
                st.session_state.hints_used = 0
                st.session_state.round_completed = False
                st.session_state.last_feedback = None
                st.rerun()
        
        with col_board:
            if st.button("📊 Leaderboard", use_container_width=True):
                st.session_state.game_state = 'leaderboard'
                st.rerun()
        
        with col_menu:
            if st.button("🏠 Main Menu", use_container_width=True):
                st.session_state.game_state = 'menu'
                st.rerun()

def show_leaderboard(db):
    st.markdown("### 🏆 Leaderboard - Top Players")
    
    scores = db.get_leaderboard()
    
    if scores:
        # Create leaderboard display
        for i, score in enumerate(scores[:10], 1):
            col1, col2, col3, col4 = st.columns([0.5, 2, 1, 1.5])
            
            with col1:
                if i == 1:
                    st.markdown("🥇")
                elif i == 2:
                    st.markdown("🥈")
                elif i == 3:
                    st.markdown("🥉")
                else:
                    st.markdown(f"**{i}**")
            
            with col2:
                st.markdown(f"**{score['player_name']}**")
            
            with col3:
                st.markdown(f"**{score['score']}** pts")
            
            with col4:
                date_str = datetime.fromisoformat(score['date_played']).strftime("%m/%d/%Y %H:%M")
                st.markdown(f"{date_str}")
    else:
        st.info("No scores recorded yet. Be the first to play!")
    
    if st.button("🏠 Back to Menu", type="primary"):
        st.session_state.game_state = 'menu'
        st.rerun()

def create_function_plot(func_data):
    """Create an interactive plot of the rational function"""
    try:
        x = symbols('x')
        expr = func_data['expression']
        
        # Create x values for plotting
        x_vals = np.linspace(-10, 10, 1000)
        y_vals = []
        
        # Evaluate function at each point
        for x_val in x_vals:
            try:
                y_val = float(expr.subs(x, x_val))
                # Limit y values to reasonable range
                if abs(y_val) > 50:
                    y_vals.append(np.nan)
                else:
                    y_vals.append(y_val)
            except:
                y_vals.append(np.nan)
        
        # Create plot
        fig = go.Figure()
        
        # Add function curve
        fig.add_trace(go.Scatter(
            x=x_vals,
            y=y_vals,
            mode='lines',
            name='f(x)',
            line=dict(color='blue', width=2),
            connectgaps=False
        ))
        
        # Add vertical asymptotes
        for va in func_data['features']['vertical_asymptotes']:
            fig.add_vline(x=va, line_dash="dash", line_color="red", 
                         annotation_text=f"x = {va}")
        
        # Add horizontal asymptote
        if func_data['features']['horizontal_asymptote'] is not None:
            ha = func_data['features']['horizontal_asymptote']
            fig.add_hline(y=ha, line_dash="dash", line_color="green", 
                         annotation_text=f"y = {ha}")
        
        # Add holes
        for hole_x, hole_y in func_data['features']['holes']:
            fig.add_trace(go.Scatter(
                x=[hole_x],
                y=[hole_y],
                mode='markers',
                marker=dict(symbol='circle-open', size=10, color='red'),
                name=f'Hole at ({hole_x}, {hole_y})'
            ))
        
        # Add intercepts
        for x_int in func_data['features']['x_intercepts']:
            fig.add_trace(go.Scatter(
                x=[x_int],
                y=[0],
                mode='markers',
                marker=dict(symbol='circle', size=8, color='orange'),
                name=f'x-intercept: {x_int}'
            ))
        
        if func_data['features']['y_intercept'] is not None:
            fig.add_trace(go.Scatter(
                x=[0],
                y=[func_data['features']['y_intercept']],
                mode='markers',
                marker=dict(symbol='circle', size=8, color='purple'),
                name=f'y-intercept: {func_data["features"]["y_intercept"]}'
            ))
        
        fig.update_layout(
            title="Rational Function Graph",
            xaxis_title="x",
            yaxis_title="y",
            xaxis=dict(range=[-8, 8], gridcolor='lightgray'),
            yaxis=dict(range=[-10, 10], gridcolor='lightgray'),
            showlegend=False,
            height=400
        )
        
        return fig
        
    except Exception as e:
        # Fallback simple plot
        fig = go.Figure()
        fig.add_annotation(
            text="Graph generation error",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig

if __name__ == "__main__":
    main()
