"""
Test suite for base repository functionality.
"""
import pytest
from unittest.mock import Mock, patch
from datetime import datetime, date

from backend.happypath.repository.base_repository import (
    BaseRepository, QueryOptions, QueryResult,
    ValidationError, NotFoundError, DuplicateError
)

class TestEntity:
    """Test entity for base repository testing."""
    def __init__(self, id=None, name=None, created_at=None):
        self.id = id
        self.name = name
        self.created_at = created_at or datetime.now()

class TestBaseRepository:
    """Test suite for BaseRepository functionality."""
    
    @pytest.fixture
    def test_repository(self, mock_db_manager, mock_logger):
        """Create test repository instance."""
        return BaseRepository(
            entity_class=TestEntity,
            db_manager=mock_db_manager,
            logger=mock_logger,
            table_name="test_entities"
        )
    
    def test_create_entity_success(self, test_repository, mock_db_manager):
        """Test successful entity creation."""
        # Arrange
        entity = TestEntity(name="Test Entity")
        mock_db_manager.execute_query.return_value = [{"id": 1, "name": "Test Entity"}]
        
        # Act
        result = test_repository.create(entity)
        
        # Assert
        assert result.id == 1
        assert result.name == "Test Entity"
        mock_db_manager.execute_query.assert_called_once()
    
    def test_create_entity_validation_error(self, test_repository):
        """Test entity creation with validation error."""
        # Arrange
        entity = TestEntity(name="")  # Invalid empty name
        
        # Act & Assert
        with pytest.raises(ValidationError):
            test_repository.create(entity)
    
    def test_get_by_id_found(self, test_repository, mock_db_manager):
        """Test successful entity retrieval by ID."""
        # Arrange
        mock_db_manager.execute_query.return_value = [{"id": 1, "name": "Test Entity"}]
        
        # Act
        result = test_repository.get_by_id(1)
        
        # Assert
        assert result is not None
        assert result.id == 1
        assert result.name == "Test Entity"
    
    def test_get_by_id_not_found(self, test_repository, mock_db_manager):
        """Test entity retrieval when not found."""
        # Arrange
        mock_db_manager.execute_query.return_value = []
        
        # Act
        result = test_repository.get_by_id(999)
        
        # Assert
        assert result is None
    
    def test_update_entity_success(self, test_repository, mock_db_manager):
        """Test successful entity update."""
        # Arrange
        entity = TestEntity(id=1, name="Updated Entity")
        mock_db_manager.execute_query.return_value = [{"id": 1, "name": "Updated Entity"}]
        
        # Act
        result = test_repository.update(entity)
        
        # Assert
        assert result.name == "Updated Entity"
        mock_db_manager.execute_query.assert_called_once()
    
    def test_delete_entity_success(self, test_repository, mock_db_manager):
        """Test successful entity deletion."""
        # Arrange
        mock_db_manager.execute_query.return_value = [{"affected_rows": 1}]
        
        # Act
        result = test_repository.delete(1)
        
        # Assert
        assert result is True
        mock_db_manager.execute_query.assert_called_once()
    
    def test_delete_entity_not_found(self, test_repository, mock_db_manager):
        """Test entity deletion when not found."""
        # Arrange
        mock_db_manager.execute_query.return_value = [{"affected_rows": 0}]
        
        # Act
        result = test_repository.delete(999)
        
        # Assert
        assert result is False
    
    def test_list_all_with_filters(self, test_repository, mock_db_manager):
        """Test listing entities with filters."""
        # Arrange
        options = QueryOptions(
            filters={"name": "Test"},
            order_by=["name"],
            limit=10
        )
        mock_db_manager.execute_query.return_value = [
            {"id": 1, "name": "Test Entity 1"},
            {"id": 2, "name": "Test Entity 2"}
        ]
        
        # Act
        result = test_repository.list_all(options)
        
        # Assert
        assert len(result.data) == 2
        assert result.data[0].name == "Test Entity 1"
        mock_db_manager.execute_query.assert_called_once()
    
    def test_find_one_by_success(self, test_repository, mock_db_manager):
        """Test finding single entity by criteria."""
        # Arrange
        mock_db_manager.execute_query.return_value = [{"id": 1, "name": "Test Entity"}]
        
        # Act
        result = test_repository.find_one_by(name="Test Entity")
        
        # Assert
        assert result is not None
        assert result.name == "Test Entity"
    
    def test_find_one_by_multiple_results_error(self, test_repository, mock_db_manager):
        """Test finding single entity when multiple results exist."""
        # Arrange
        mock_db_manager.execute_query.return_value = [
            {"id": 1, "name": "Test Entity"},
            {"id": 2, "name": "Test Entity"}
        ]
        
        # Act & Assert
        with pytest.raises(ValueError, match="Multiple entities found"):
            test_repository.find_one_by(name="Test Entity")
    
    def test_exists_true(self, test_repository, mock_db_manager):
        """Test entity existence check returns True."""
        # Arrange
        mock_db_manager.execute_query.return_value = [{"count": 1}]
        
        # Act
        result = test_repository.exists(id=1)
        
        # Assert
        assert result is True
    
    def test_exists_false(self, test_repository, mock_db_manager):
        """Test entity existence check returns False."""
        # Arrange
        mock_db_manager.execute_query.return_value = [{"count": 0}]
        
        # Act
        result = test_repository.exists(id=999)
        
        # Assert
        assert result is False
    
    def test_count_entities(self, test_repository, mock_db_manager):
        """Test counting entities with filters."""
        # Arrange
        mock_db_manager.execute_query.return_value = [{"count": 5}]
        
        # Act
        result = test_repository.count(name="Test")
        
        # Assert
        assert result == 5
    
    def test_transaction_success(self, test_repository, mock_db_manager):
        """Test successful transaction execution."""
        # Arrange
        entity = TestEntity(name="Transaction Test")
        mock_db_manager.execute_query.return_value = [{"id": 1, "name": "Transaction Test"}]
        
        # Act
        with test_repository.transaction():
            result = test_repository.create(entity)
        
        # Assert
        assert result.name == "Transaction Test"
        mock_db_manager.begin_transaction.assert_called_once()
        mock_db_manager.commit_transaction.assert_called_once()
    
    def test_transaction_rollback_on_error(self, test_repository, mock_db_manager):
        """Test transaction rollback on error."""
        # Arrange
        mock_db_manager.execute_query.side_effect = Exception("Database error")
        
        # Act & Assert
        with pytest.raises(Exception):
            with test_repository.transaction():
                test_repository.create(TestEntity(name="Test"))
        
        mock_db_manager.rollback_transaction.assert_called_once()
