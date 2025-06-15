import logging
from meta_kernel.problem_miner import mine_problems
from meta_kernel.solution_designer import design_solution
from meta_kernel.business_composer import design_biz_model
from meta_kernel.spec_generator import generate_saas_spec
from meta_kernel.venture_launcher import launch_venture
from meta_kernel.growth_evaluator import evaluate_performance


def main() -> None:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
    logging.info("Starting Meta Operator pipeline")

    problem = mine_problems()
    logging.info(f"Problem mined: {problem}")

    solution = design_solution(problem)
    logging.info("Solution designed")

    biz_model = design_biz_model(solution)
    logging.info("Business model designed")

    spec = generate_saas_spec(solution, biz_model)
    logging.info("Spec generated")

    launch_venture(spec)
    logging.info("Venture launched")

    _ = evaluate_performance("portfolio")
    logging.info("Performance evaluated")


if __name__ == "__main__":
    main()
