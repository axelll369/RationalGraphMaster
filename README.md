# Graph Quest: Rational Rampage

An interactive educational game built with Streamlit for learning rational function graphing concepts including asymptotes, holes, and intercepts.

## Features

- **5 Progressive Difficulty Rounds**: From simple vertical asymptotes to complex rational functions
- **Interactive Gameplay**: Identify key features like vertical/horizontal asymptotes, holes, and intercepts
- **Real-time Feedback**: Instant scoring and detailed explanations
- **Leaderboard System**: Track high scores and player statistics
- **Mathematical Visualization**: Interactive Plotly graphs with function features highlighted
- **Hint System**: Get educational hints when stuck (with point penalties)

## Installation

### Local Installation

1. Clone this repository:
```bash
git clone [your-repo-url]
cd rational-rampage
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

### Dependencies

- **streamlit** >= 1.28.0 - Web framework
- **matplotlib** >= 3.5.0 - Plotting library
- **plotly** >= 5.0.0 - Interactive graphs
- **sympy** >= 1.10.0 - Symbolic mathematics
- **numpy** >= 1.21.0 - Numerical computing

## How to Play

1. Enter your name and click "Start Game"
2. Analyze the given rational function
3. Identify and input:
   - Vertical asymptotes (x-values)
   - Horizontal asymptote (y-value or "none")
   - Holes (x-values or "none")
   - X-intercepts (x-values or "none")
   - Y-intercept (y-value or "undefined")
4. Submit answers to get immediate feedback
5. Progress through 5 rounds of increasing difficulty
6. View your final score and leaderboard ranking

## Educational Content

The game covers essential precalculus concepts:
- **Vertical Asymptotes**: Values where the function approaches infinity
- **Horizontal Asymptotes**: End behavior of rational functions
- **Holes**: Removable discontinuities in rational functions
- **Intercepts**: Where the function crosses the axes
- **Function Analysis**: Understanding rational function behavior

## Scoring System

- **100 points** per correct feature identification
- **-10 points** per hint used
- **Bonus achievements** for exceptional performance
- **Progressive difficulty** with more complex functions in later rounds

## File Structure

```
├── app.py                 # Main Streamlit application
├── game_logic.py          # Game mechanics and scoring
├── function_generator.py  # Rational function generation
├── database.py           # Score storage and leaderboard
├── requirements.txt      # Python dependencies
└── leaderboard.json      # Score data (auto-generated)
```

## Deployment

### Streamlit Cloud
1. Push code to GitHub
2. Connect to Streamlit Cloud
3. Deploy with requirements.txt

### Local Sharing
The app runs on `localhost:8501` by default and can be accessed by anyone on your local network.

## Contributing

This educational tool is designed for precalculus students learning rational functions. Contributions welcome for:
- Additional function types
- Enhanced visualizations
- Improved educational content
- Bug fixes and optimizations

## License

Educational use encouraged. Built with Streamlit for interactive mathematics education.