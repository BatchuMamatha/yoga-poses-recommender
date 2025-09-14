import logging
import json
import io
import urllib.parse
from flask import Flask, request, jsonify, render_template, make_response
import google.generativeai as genai
import pyttsx3
from settings import get_settings

settings = get_settings()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

app = Flask(__name__)

# Configure Gemini API
if settings.gemini_api_key and settings.gemini_api_key != "YOUR_GEMINI_API_KEY_HERE":
    genai.configure(api_key=settings.gemini_api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None
    logging.warning("Gemini API key not configured. Some features will be disabled.")

# Load local yoga poses data
def load_local_yoga_data():
    """Load yoga poses from local JSON file"""
    try:
        with open('./data/yoga_poses_with_descriptions_full.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            logging.info("✅ Using complete dataset with descriptions: yoga_poses_with_descriptions_full.json")
            return data
    except FileNotFoundError:
        logging.error("yoga_poses_with_descriptions_full.json not found!")
        return []

yoga_poses = load_local_yoga_data()
logging.info(f"Loaded {len(yoga_poses)} yoga poses from local data")

def simple_search(query: str):
    """Enhanced text-based search through yoga poses with better matching"""
    query_lower = query.lower()
    query_words = query_lower.split()
    results = []
    scored_results = []
    
    # Debug logging for search
    logging.info(f"Search query: '{query}' | Words: {query_words}")
    
    # Keywords for different types of searches
    back_pain_keywords = ['back', 'spine', 'lower back', 'upper back', 'backache']
    beginner_keywords = ['beginner', 'easy', 'simple', 'basic', 'start']
    flexibility_keywords = ['flexible', 'stretch', 'stretching', 'flexibility']
    strength_keywords = ['strong', 'strength', 'muscle', 'power']
    relaxation_keywords = ['relax', 'calm', 'peace', 'stress', 'anxiety']
    balance_keywords = ['balance', 'stability', 'equilibrium']
    
    for pose in yoga_poses:
        score = 0
        
        # Get all searchable text
        name = pose.get('name', '').lower()
        sanskrit_name = pose.get('sanskrit_name', '').lower()
        pose_types = [t.lower() for t in pose.get('pose_type', [])]
        expertise = pose.get('expertise_level', '').lower()
        description = pose.get('description', '').lower()
        
        # Create combined searchable text
        all_text = f"{name} {sanskrit_name} {' '.join(pose_types)} {expertise} {description}"
        
        # Debug for specific poses we're interested in
        if any(word in name for word in ['gorilla', 'child', 'warrior']):
            logging.info(f"Checking pose: {pose.get('name', 'Unknown')} | name: '{name}'")
        
        # Direct word matches (highest priority)
        for word in query_words:
            if word in name:
                score += 10  # High score for name matches
                if any(debug_word in name for debug_word in ['gorilla', 'child', 'warrior']):
                    logging.info(f"  Match in name '{name}' for word '{word}': +10 points (total: {score})")
            elif word in sanskrit_name:
                score += 8
            elif word in ' '.join(pose_types):
                score += 6
            elif word in expertise:
                score += 5
            elif word in description:
                score += 3
            elif word in all_text:
                score += 1
        
        # Special keyword matching for common queries
        if any(keyword in query_lower for keyword in back_pain_keywords):
            if any(pt in ['forward bend', 'twist', 'backbend'] for pt in pose_types):
                score += 8
            if 'child' in name or 'downward' in name or 'cat' in name or 'cobra' in name:
                score += 10
                
        if any(keyword in query_lower for keyword in beginner_keywords):
            if expertise == 'beginner':
                score += 10
                
        if any(keyword in query_lower for keyword in balance_keywords):
            if any(pt in ['balancing', 'standing'] for pt in pose_types):
                score += 8
                
        if any(keyword in query_lower for keyword in flexibility_keywords):
            if any(pt in ['forward bend', 'hip opener', 'twist'] for pt in pose_types):
                score += 8
                
        if any(keyword in query_lower for keyword in strength_keywords):
            if any(pt in ['arm balance', 'inversion', 'standing'] for pt in pose_types):
                score += 8
                
        if any(keyword in query_lower for keyword in relaxation_keywords):
            if any(pt in ['restorative', 'seated'] for pt in pose_types):
                score += 8
        
        # Add poses with any score > 0
        if score > 0:
            scored_results.append((score, pose))
    
    # Sort by score (highest first) and take top results
    scored_results.sort(key=lambda x: x[0], reverse=True)
    
    # Debug logging for top results
    if scored_results:
        logging.info(f"Top 5 search results for '{query}':")
        for i, (score, pose) in enumerate(scored_results[:5]):
            logging.info(f"  {i+1}. {pose.get('name', 'Unknown')} (score: {score})")
    else:
        logging.info(f"No results found for '{query}'")
    
    # Ensure we have at least 3 results by including poses with score 0 if needed
    available_results = scored_results if scored_results else []
    
    # If we have fewer than 3 results, add random poses to reach 3
    if len(available_results) < 3:
        # Get poses not already in results
        used_poses = {pose.get('name', '') for score, pose in available_results}
        unused_poses = [pose for pose in yoga_poses if pose.get('name', '') not in used_poses]
        
        # Add random unused poses with score 0
        import random
        additional_needed = 3 - len(available_results)
        random_poses = random.sample(unused_poses, min(additional_needed, len(unused_poses)))
        
        for pose in random_poses:
            available_results.append((0, pose))
        
        logging.info(f"Added {len(random_poses)} random poses to reach minimum 3 results")
    
    # Take top 3 results and format them
    for score, pose in available_results[:3]:
        # Generate a simple description if none exists
        if not pose.get('description'):
            description = f"This is a {pose.get('expertise_level', 'yoga')} level {' and '.join(pose.get('pose_type', ['yoga']))} pose called {pose.get('name', 'Unknown')}."
        else:
            description = pose.get('description', '')
            
        # Ensure description is not empty
        if not description.strip():
            description = f"This is a {pose.get('expertise_level', 'yoga')} level {' and '.join(pose.get('pose_type', ['yoga']))} pose called {pose.get('name', 'Unknown')}."
        
        result = {
            "page_content": f"name: {pose.get('name', '')}\ndescription: {description}\nsanskrit_name: {pose.get('sanskrit_name', '')}\nexpertise_level: {pose.get('expertise_level', '')}\npose_type: {', '.join(pose.get('pose_type', []))}",
            "metadata": {"metadata": {**pose, "description": description}}
        }
        results.append(result)
    
    return results[:3]  # Always return exactly 3 results

@app.route("/", methods=["GET"])
def index():
    """Renders the HTML page with the search form."""
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search_api():
    """API endpoint to search documents based on the prompt provided in json"""
    try:
        data = request.get_json()
        if not data or "prompt" not in data:
            return jsonify({"error": "Missing prompt in request body"}), 400
        
        prompt = data["prompt"]
        logging.info(f"Searching for: {prompt}")
        
        # Use simple text search instead of vector search
        results = simple_search(prompt)
        
        return jsonify({"results": results}), 200
    except Exception as e:
        logging.error(f"Error during search: {e}")
        return jsonify({"error": "An error occurred during search"}), 500

@app.route('/generate_audio', methods=['POST'])
def generate_audio():
    """Generate audio using local Text-to-Speech"""
    try:
        data = request.get_json()
        description = data.get('description')
        if not description:
            logging.error("No description provided for audio generation")
            return jsonify({'error': 'Missing description'}), 400

        # Decode URL-encoded description and clean it
        decoded_description = urllib.parse.unquote(description)
        # Clean the description - remove any problematic characters
        decoded_description = ''.join(char for char in decoded_description if ord(char) < 127)  # Keep only ASCII
        decoded_description = decoded_description.replace('\n', ' ').replace('\r', ' ')  # Replace newlines
        decoded_description = ' '.join(decoded_description.split())  # Normalize whitespace
        
        # Limit description length to prevent very long audio
        if len(decoded_description) > 500:
            decoded_description = decoded_description[:500] + "..."
        
        logging.info(f"Generating audio for: {decoded_description[:100]}...")
        
        # Log the cleaned description for debugging
        if len(decoded_description) != len(urllib.parse.unquote(description)):
            logging.info(f"Description cleaned from {len(urllib.parse.unquote(description))} to {len(decoded_description)} characters")
        
        # Initialize local TTS engine
        try:
            engine = pyttsx3.init()
        except Exception as init_error:
            logging.error(f"Failed to initialize pyttsx3: {init_error}")
            return jsonify({'error': 'Text-to-speech engine not available'}), 500
        
        # Set properties for better audio quality
        try:
            engine.setProperty('rate', 140)  # Slightly slower for clarity
            engine.setProperty('volume', 0.9)  # Higher volume
            
            # Get available voices and set a pleasant voice
            voices = engine.getProperty('voices')
            if voices and len(voices) > 1:
                # Try to use a female voice (usually index 1)
                engine.setProperty('voice', voices[1].id)
            elif voices and len(voices) > 0:
                engine.setProperty('voice', voices[0].id)
                
        except Exception as voice_error:
            logging.warning(f"Could not set voice properties: {voice_error}")
            # Continue with default settings
        
        # Create a temporary file for the audio
        import tempfile
        import os
        import time
        
        # Create temp file with timestamp to avoid conflicts
        timestamp = int(time.time() * 1000)
        temp_dir = tempfile.gettempdir()
        temp_filename = os.path.join(temp_dir, f'yoga_audio_{timestamp}.wav')
        
        try:
            # Save speech to file
            engine.save_to_file(decoded_description, temp_filename)
            engine.runAndWait()
            
            # Wait a moment for file to be fully written
            time.sleep(0.5)
            
            # Check if file was created and has content
            if not os.path.exists(temp_filename):
                raise Exception("Audio file was not created")
                
            file_size = os.path.getsize(temp_filename)
            if file_size == 0:
                raise Exception("Audio file is empty")
                
            logging.info(f"Generated audio file: {temp_filename} (size: {file_size} bytes)")
            
            # Read the audio file and return it
            with open(temp_filename, 'rb') as audio_file:
                audio_content = audio_file.read()
            
            # Clean up temp file
            try:
                os.unlink(temp_filename)
            except:
                pass  # Ignore cleanup errors
            
            if not audio_content:
                raise Exception("No audio content generated")
            
            # Return audio content with proper headers
            response = make_response(audio_content)
            response.headers.set('Content-Type', 'audio/wav')
            response.headers.set('Content-Length', str(len(audio_content)))
            response.headers.set('Cache-Control', 'no-cache')
            
            logging.info(f"Successfully generated audio: {len(audio_content)} bytes")
            return response
            
        except Exception as generation_error:
            logging.error(f"Error during audio generation: {generation_error}")
            # Clean up temp file if it exists
            try:
                if os.path.exists(temp_filename):
                    os.unlink(temp_filename)
            except:
                pass
            return jsonify({'error': f'Failed to generate audio: {str(generation_error)}'}), 500
        
        finally:
            # Cleanup engine
            try:
                engine.stop()
            except:
                pass
            
    except Exception as e:
        logging.error(f"Unexpected error in audio generation: {e}")
        return jsonify({'error': f'Audio generation failed: {str(e)}'}), 500

@app.route('/test_audio')
def test_audio():
    """Test audio generation with a simple message"""
    try:
        # Test if pyttsx3 is working
        import pyttsx3
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        audio_info = {
            'pyttsx3_available': True,
            'voices_count': len(voices) if voices else 0,
            'voices': []
        }
        
        if voices:
            for i, voice in enumerate(voices[:3]):  # Show first 3 voices
                audio_info['voices'].append({
                    'index': i,
                    'id': voice.id,
                    'name': getattr(voice, 'name', 'Unknown'),
                    'languages': getattr(voice, 'languages', [])
                })
        
        engine.stop()
        return jsonify(audio_info)
        
    except Exception as e:
        return jsonify({
            'pyttsx3_available': False,
            'error': str(e)
        })

@app.route('/debug_pose/<pose_name>')
def debug_pose(pose_name):
    """Debug a specific pose and its description"""
    try:
        # Find the pose in the dataset
        matching_poses = [pose for pose in yoga_poses if pose_name.lower() in pose.get('name', '').lower()]
        
        if not matching_poses:
            return jsonify({'error': f'No pose found matching: {pose_name}'})
        
        pose = matching_poses[0]
        description = pose.get('description', 'No description available')
        
        return jsonify({
            'name': pose.get('name'),
            'sanskrit_name': pose.get('sanskrit_name'),
            'description': description,
            'description_length': len(description),
            'has_special_chars': any(ord(char) > 126 for char in description),
            'cleaned_description': ''.join(char for char in description if ord(char) < 127),
            'expertise_level': pose.get('expertise_level'),
            'pose_type': pose.get('pose_type')
        })
        
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/test_search/<query>')
def test_search_endpoint(query):
    """Test search endpoint that returns results as JSON"""
    try:
        results = simple_search(query)
        return jsonify({
            'query': query,
            'num_results': len(results),
            'results': results
        })
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(settings.port))