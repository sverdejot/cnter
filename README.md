# 🔢 cnter: a counter-based social app

Sample project to practice and establish all the knowledge acquired about DevOps culture. 

Focused on applying different 🛠️ design patterns (DDD, TDD, BDD...) and implementing alternatives to monoliths apps (CQRS-microservices). Also, learning key 👷‍♂️ operational concepts like CI/CD, deploy and orchestrate containers, fault-tolerance, high-avaliability, high-scalability...

Tech stack used (by this time):
* `FastAPI`
* `MongoDB` (with `Motor` for async I/O)
* `pytest`
* `behance`
* GH actions

# Local deployment
To test the app locally, Docker is required. Simply, open up a `terminal` and execute

```bash
docker compose up
```

And access 📚 `http:localhost:8000/docs` to see which operations are available

# References:
* [*Building Microservices*](https://www.amazon.com/Building-Microservices-Designing-Fine-Grained-Systems/dp/1492034029) by Newman.
* [*Architecture Patterns with Python*](https://www.amazon.com/Architecture-Patterns-Python-Domain-Driven-Microservices/dp/1492052205) by Percival & Gregory.
* [*Implementing Domain-Driven design*](https://www.amazon.com/-/es/Vaughn-Vernon/dp/0321834577) by Vernon
* [*CodelyTV* courses](https://codely.com/)