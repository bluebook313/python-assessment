# Git Commit Message Best Practices

## 1. Recommended Format

Use this format for most commits:

```text
<type>(relative path): <short description>
```

Example:

```text
feat(service/auth/auth.py): add JWT authentication
```

---

## 2. Commit Types

Use a consistent type to describe what the commit does.

| Type       | Meaning                               | Example                                      |
| ---------- | ------------------------------------- | -------------------------------------------- |
| `feat`     | Add a new feature                     | `feat(user): add user registration`          |
| `fix`      | Fix a bug                             | `fix(auth): handle expired JWT tokens`       |
| `refactor` | Change code without changing behavior | `refactor(api): simplify request validation` |
| `docs`     | Documentation changes                 | `docs(readme): add installation guide`       |
| `test`     | Add or modify tests                   | `test(user): add registration tests`         |
| `chore`    | Maintenance tasks                     | `chore: update dependencies`                 |
| `build`    | Build system changes                  | `build: update Docker image`                 |
| `perf`     | Performance improvement               | `perf(db): optimize user query`              |
| `style`    | Formatting/style only                 | `style: format Python files`                 |


---

## 3. Good Commit Messages Sample

```text
feat(user): add user registration endpoint
```

```text
feat(auth): implement JWT authentication
```
