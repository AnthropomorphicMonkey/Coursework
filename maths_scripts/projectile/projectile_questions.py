import scripts.question_scripts
import maths_scripts.projectile.projectile_2d as projectile_2d
def q(name: str, difficulty: int, question_text: str):
    projectile = projectile_2d.Projectile()
    correct_answer = ""
    question_text = ""
    question = scripts.question_scripts.Question(name, None, difficulty, question_text)