class CreateCombinations < ActiveRecord::Migration[5.1]
  def change
    create_table :combinations do |t|
      t.integer :micropost_id
      t.integer :tag_id

      t.timestamps
    end
    add_index :combinations, :micropost_id
    add_index :combinations, :tag_id
    add_index :combinations, [:micropost_id, :tag_id], unique: true
  end
end
