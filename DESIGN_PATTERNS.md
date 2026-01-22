# Design Patterns

## 1) Singleton
**Idea:** Ensures a class has **only one instance** and provides a global access point to it.  
**When to use:** Shared resources such as configuration, a logger, or a connection pool.  
**Downside:** Can make testing harder and may behave like hidden global state.

---

## 2) Factory Method
**Idea:** Defines a method for creating objects, but lets subclasses/implementations decide **which concrete class** to instantiate.  
**When to use:** When you have a common interface (e.g., `Parser`) but the concrete type (JSON/XML/CSV) depends on input or configuration.

---

## 3) Strategy
**Idea:** Encapsulates multiple algorithms behind a common interface and allows switching them **at runtime** without large `if/else` blocks.  
**When to use:** Different pricing/discount rules, validation logic, sorting methods, routing rules, etc.

---

## 4) Observer
**Idea:** Allows “observers” (subscribers) to register to a “subject”. When the subject changes, it **notifies** all observers.  
**When to use:** Event-driven systems, UI updates, notifications, pub/sub style architectures.

---

## 5) Decorator
**Idea:** Adds extra behavior to an object **dynamically** by wrapping it, without modifying the original class.  
**When to use:** Logging, caching, authorization checks, and adding features in layers.
